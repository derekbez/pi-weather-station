Raspberry Pi Weather Station

This is based on the Raspberry Pi Foundation weather station, as found here:
https://projects.raspberrypi.org/en/projects/build-your-own-weather-station/1

##########
PRE-REQS:

Noobs
Raspbian 
Lite - no GUI is best

sudo apt update
sudo apt full-upgrade

change password 
passwd

(Install git and pip):
sudo apt-get install git
sudo apt install python3-pip

git clone https://github.com/derekbez/pi-weather-station.git

sudo raspi-config
Interfacing Options:
SSH
SPI
I2C
1-Wire

Boot Options > Desktop / CLI > Console Autologin

Install the BME280 Python library for the temperature, pressure, humidity sensor:
sudo pip3 install RPi.bme280

sudo apt install python3-gpiozero

For the DS18B20 thermal probe sensor:
sudo nano /boot/config.txt
Edit it by adding the line below at the bottom:
dtoverlay=w1-gpio

sudo nano /etc/modules
Add the lines below at the bottom of the file:
w1-gpio
w1-therm

Install the MariaDB database server software:
sudo apt-get install -y mariadb-server mariadb-client libmariadbclient-dev
sudo pip3 install mysqlclient



##########
(INSTALLING IN A VIRTUAL ENVIRONMENT):

python3 -m venv d:\dev\pi-weather-station

.\scripts\activate

python3 --version

copy requirements.txt 
   (pip freeze > requirements.txt)
   
python3 -m pip install --upgrade pip


##########
(RUN ON BOOT):
https://www.dexterindustries.com/howto/run-a-program-on-your-raspberry-pi-at-startup/

sudo nano /lib/systemd/system/weather.service
add this:
---
[Unit]
Description=Weather Station Service
After=multi-user.target

[Service]
Type=idle
ExecStart=/usr/bin/python3 /home/pi/pi-weather-station/weather-station.py

[Install]
WantedBy=multi-user.target
--- 
 
sudo chmod 644 /lib/systemd/system/weather.service 
sudo systemctl daemon-reload
sudo systemctl enable weather.service 
sudo reboot

Check if running:
ps aux | grep weather-station

##########
SENSORS:

BME280 Temperature, Pressue and Humidity sensor
The I2C address is 0x76 on the unit I'm using.

Pins connected as follows:
17 (3V3)	Vin
6 (Gnd)	Gnd
3 (SDA)	SDA (SDI)
5 (SCL)	SCL (SCK)

DS18B20  Ground temperature probe
Uses code from the RPi GitHub repository for this project (ds18b20_therm.py).  Hence the LICENSE file included.

Wind Speed, Wind Direction and Rainfall
Code implemented, but no sensors connected.

########## 
DATABASE:

sudo mysql

create user pi IDENTIFIED by 'my54cr4t';

grant all privileges on *.* to 'pi' with grant option;

create database weather;

use weather;

CREATE TABLE WEATHER_MEASUREMENT(
ID BIGINT NOT NULL AUTO_INCREMENT,
REMOTE_ID BIGINT,
AMBIENT_TEMPERATURE DECIMAL(6,2) NOT NULL,
GROUND_TEMPERATURE DECIMAL(6,2) NOT NULL,
AIR_QUALITY DECIMAL(6,2) NOT NULL,
AIR_PRESSURE DECIMAL(6,2) NOT NULL,
HUMIDITY DECIMAL(6,2) NOT NULL,
WIND_DIRECTION DECIMAL(6,2) NULL,
WIND_SPEED DECIMAL(6,2) NOT NULL,
WIND_GUST_SPEED DECIMAL(6,2) NOT NULL,
RAINFALL DECIMAL (6,2) NOT NULL,
CREATED TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
PRIMARY KEY ( ID )
);

Check that the credentials are stored correctly in
home/pi/weather-station/credentials.mysql


select count(*) from WEATHER_MEASUREMENT;
select * from WEATHER_MEASUREMENT order by CREATED desc limit 25;


##########

https://help.github.com/en/github/importing-your-projects-to-github/adding-an-existing-project-to-github-using-the-command-line



