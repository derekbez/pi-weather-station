Raspberry Pi Weather Station

This is based on the Raspberry Pi Foundation weather station, as found here:
https://projects.raspberrypi.org/en/projects/build-your-own-weather-station/1


PRE-REQS:

sudo raspi-config
Interfacing Options:
SSH
I2C
1-Wire

Install the BME280 Python library for the temperature, pressure, humidity sensor:
sudo pip3 install RPi.bme280

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




https://help.github.com/en/github/importing-your-projects-to-github/adding-an-existing-project-to-github-using-the-command-line




