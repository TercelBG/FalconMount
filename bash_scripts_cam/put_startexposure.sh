#!/bin/bash


echo "last value type is: $1"
echo "last value is: $2"
echo "Parameter 1 name is: $3"
echo "Parameter 1 type is: $4"
echo "Parameter 1 value is: $5"


# query="select value  from properties  WHERE (name = 'subexposureduration');"
# duration_row=$(mariadb -u alpaca -pdobri4 -D alpaca_camera -e "$query")
# duraion=$(echo $duration_row | awk '{print $2}')
query="UPDATE properties SET value = 'False' WHERE (name = 'imageready');"
mariadb -u alpaca -pdobri4 -D alpaca_camera -e "$query"


query="UPDATE properties SET value = '2' WHERE (name = 'camerastate');"
mariadb -u alpaca -pdobri4 -D alpaca_camera -e "$query"

time="$(date +'%d_%m_%Y_%H_%M_%S')"
date="$(date +'%Y%m%d')"
filename="/mnt/photos/$date/light_$time"
cpfilename="light_$time"
#gphoto2 -B $5 --capture-and-download f
# query="UPDATE properties SET value = '2' WHERE (name = 'camerastate');"
# mariadb -u alpaca -pdobri4 -D alpaca_camera -e "$query" 

/usr/bin/gphoto2 -B $5 --capture-image-and-download --filename "$filename.%C" 
 rm /opt/alpaca/bash_scripts_cam/*.NEF
 cp $filename.NEF /opt/alpaca/bash_scripts_cam/$cpfilename.NEF
echo  "filenameparam is '$filename'"
query="UPDATE properties SET value = 'bash_scripts_cam/$cpfilename.NEF' WHERE (name = 'imagearray');"
mariadb -u alpaca -pdobri4 -D alpaca_camera -e "$query"
query="UPDATE properties SET value = 'True' WHERE (name = 'imageready');"
mariadb -u alpaca -pdobri4 -D alpaca_camera -e "$query"
query="UPDATE properties SET value = '0' WHERE (name = 'camerastate');"
mariadb -u alpaca -pdobri4 -D alpaca_camera -e "$query"

exit 0