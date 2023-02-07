#!/bin/bash

#start the pigio demon


echo "type is: $1"
echo "last value is: $2"
echo "Parameter 1 name is: $3"
echo "Parameter 1 type is: $4"
echo "Parameter 1 value is: $5"
echo "Parameter 2 value is: $6"


query="UPDATE properties SET value = 'True' WHERE (name = 'slewing');"
# query="UPDATE properties SET value = 'False' WHERE (name = 'tracking');"
mariadb -u alpaca -pdobri4 -D alpaca_scope -e "$query"

if [ "$5" == "0" ]; then
    sudo python3 hardwarecontrol/movera.py $6
elif [ "$5" == "1" ]; then
    sudo python3 hardwarecontrol/movedec.py $6
fi



exit 0