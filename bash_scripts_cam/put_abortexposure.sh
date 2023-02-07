#!/bin/bash


echo "last value type is: $1"
echo "last value is: $2"
echo "Parameter 1 name is: $3"
echo "Parameter 1 type is: $4"
echo "Parameter 1 value is: $5"


# query="select value  from properties  WHERE (name = 'subexposureduration');"
# duration_row=$(mariadb -u alpaca -pdobri4 -D alpaca_camera -e "$query")
# duraion=$(echo $duration_row | awk '{print $2}')
/usr/bin/gphoto2 -B $5 --capture-image-and-download --filename "$filename.%C"


query="UPDATE properties SET value = '1' WHERE (name = 'camerastate');"
mariadb -u alpaca -pdobri4 -D alpaca_camera -e "$query"


exit 0