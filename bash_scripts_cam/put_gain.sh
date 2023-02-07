#!/bin/bash



echo "last value type is: $1"
echo "last value is: $2"
echo "Parameter 1 name is: $3"
echo "Parameter 1 type is: $4"
echo "Parameter 1 value is: $5"

if [ $5 == "None" ]; then
    /usr/bin/gphoto2 --set-config iso=100
    query="UPDATE properties SET value = '0' WHERE (name = 'gain');"
    mariadb -u alpaca -pdobri4 -D alpaca_camera -e "$query"
elif [ $5 == "0" ]; then
    /usr/bin/gphoto2 --set-config iso=100
    query="UPDATE properties SET value = '$5' WHERE (name = 'gain');"
    mariadb -u alpaca -pdobri4 -D alpaca_camera -e "$query"
elif [ $5 == "1" ]; then
    /usr/bin/gphoto2 --set-config iso=200
    query="UPDATE properties SET value = '$5' WHERE (name = 'gain');"
    mariadb -u alpaca -pdobri4 -D alpaca_camera -e "$query"
elif [ $5 == "2" ]; then
    /usr/bin/gphoto2 --set-config iso=400
    query="UPDATE properties SET value = '$5' WHERE (name = 'gain');"
    mariadb -u alpaca -pdobri4 -D alpaca_camera -e "$query"
elif [ $5 == "3" ]; then
    /usr/bin/gphoto2 --set-config iso=800
    query="UPDATE properties SET value = '$5' WHERE (name = 'gain');"
    mariadb -u alpaca -pdobri4 -D alpaca_camera -e "$query"
elif [ $5 == "4" ]; then
    /usr/bin/gphoto2 --set-config iso=1600
    query="UPDATE properties SET value = '$5' WHERE (name = 'gain');"
    mariadb -u alpaca -pdobri4 -D alpaca_camera -e "$query"
elif [ $5 == "5" ]; then
    /usr/bin/gphoto2 --set-config iso=3200
    query="UPDATE properties SET value = '$5' WHERE (name = 'gain');"
    mariadb -u alpaca -pdobri4 -D alpaca_camera -e "$query"
elif [ $5 == "6" ]; then
    /usr/bin/gphoto2 --set-config iso=6400
    query="UPDATE properties SET value = '$5' WHERE (name = 'gain');"
    mariadb -u alpaca -pdobri4 -D alpaca_camera -e "$query"
else 
    /usr/bin/gphoto2 --set-config iso=100
    query="UPDATE properties SET value = '0' WHERE (name = 'gain');"
    mariadb -u alpaca -pdobri4 -D alpaca_camera -e "$query"
fi

#mariadb -u alpaca -pdobri4 -D alpaca_camera -e "$query"

exit 0