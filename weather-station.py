#! /usr/bin/env python3

import math
import time
import datetime
import statistics
import bme280
import smbus2
from gpiozero import Button
import ds18b20_therm  # part of the RaspberryPiFoundation code
import database       #
import wind_direction  # module

CM_IN_A_KM = 100000.0
SECS_IN_AN_HOUR = 3600
ADJUSTMENT = 1.18
BUCKET_SIZE = 0.2794

interval = 300
wind_interval = 60

wind_count = 0
radius_cm = 9.0
store_speeds = []
store_directions = []
rain_count = 0
gust = 0

#temp / pressure / humidity
port = 1
address = 0x76
bus = smbus2.SMBus(port)
calibration_params = bme280.load_calibration_params(bus, address)

def read_bme280():
    data = bme280.sample(bus, address, calibration_params)
    return data.humidity, data.pressure, data.temperature

#ground temp
temp_probe = ds18b20_therm.DS18B20()


def spin():
    global wind_count
    wind_count = wind_count + 1

def calculate_speed(time_sec):
    global wind_count
    circumference_cm = (2 * math.pi) * radius_cm
    rotations = wind_count / 2.0
    dist_cm = circumference_cm * rotations
    speed = dist_cm / time_sec
    dist_km = (circumference_cm * rotations) / CM_IN_A_KM
    km_per_sec = dist_km / time_sec
    km_per_hour = km_per_sec * SECS_IN_AN_HOUR
    return km_per_hour * ADJUSTMENT

def bucket_tipped():
    global rain_count
    rain_count = rain_count + 1
    #print (rain_count * BUCKET_SIZE)

def reset_wind():
    global wind_count
    wind_count = 0

def reset_rainfall():
    global rain_count
    rain_count = 0

def reset_gust():
    global gust
    gust = 0

wind_speed_sensor = Button(5)
wind_speed_sensor.when_activated = spin

rain_sensor = Button(6)
rain_sensor.when_pressed = bucket_tipped

temp_probe = ds18b20_therm.DS18B20()

db = database.weather_database()

while True:
    start_time = time.time()
    while  time.time() - start_time <= interval:
        wind_start_time = time.time()
        reset_wind()
        #time.sleep(wind_interval)
        while time.time() - wind_start_time <= wind_interval:
            store_directions.append(wind_direction.get_value( int(wind_interval / 10 )))

        final_speed = calculate_speed(wind_interval)
        store_speeds.append(final_speed)
    wind_average = wind_direction.get_average(store_directions)
    wind_gust = max(store_speeds)
    wind_speed = statistics.mean(store_speeds)

    rainfall = rain_count * BUCKET_SIZE
    reset_rainfall()

    humidity, pressure, ambient_temp = read_bme280()
    ground_temp = temp_probe.read_temp()

    #print(wind_speed, wind_gust, rainfall, wind_average, humidity, pressure, ambient_temp, ground_temp)
    print(ambient_temp, ground_temp, 0, pressure, humidity, wind_average, wind_speed, wind_gust, rainfall, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    db.insert(ambient_temp, ground_temp, 0, pressure, humidity, wind_average, wind_speed, wind_gust, rainfall, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    store_speeds = []
    store_directions = []


