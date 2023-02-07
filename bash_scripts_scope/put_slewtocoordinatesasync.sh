#!/bin/bash



echo "last value type is: $1"
echo "last value is: $2"
echo "Parameter 1 name is: $3"
echo "Parameter 1 type is: $4"
echo "Parameter 1 value is: $5"



query="select value  from properties  WHERE (name = 'rightascension');"
currentra=$(mariadb -u alpaca -pdobri4 -D alpaca_scope -e "$query")

query="select value  from properties  WHERE (name = 'declination');"
currentdec=$(mariadb -u alpaca -pdobri4 -D alpaca_scope -e "$query")

query="update properties set value = 'True'  WHERE (name = 'slewing');"
mariadb -u alpaca -pdobri4 -D alpaca_scope -e "$query"

query="select value  from properties  WHERE (name = 'tracking');"
tracking=$(mariadb -u alpaca -pdobri4 -D alpaca_scope -e "$query")

currentra=$(echo $currentra | awk '{print $2}')
currentdec=$(echo $currentdec | awk '{print $2}')
tracking=$(echo $tracking | awk '{print $2}')

echo "current RA is: $currentra "
echo "current DEC is: $currentdec "
echo "Tracking is: $tracking "

# Print the values
sudo python3 hardwarecontrol/slewasync.py $currentra $currentdec $5 $6 $tracking

#get current coordinates from the database

#calc the time for the rate

#start time 
#slew slewing
#constantly update coordinates until slewing ends

#check if tracking is True
# if [ "$5" == "True" ]; then
#     python hardwarecontrol/start_tracking.py
# else
#     sudo killall pigpiod
#     sudo pigpiod
#     sudo chown alex:alex /var/run/pigpio.pid
#     sudo python hardwarecontrol/stop_tracking.py
# fi

# query="UPDATE properties SET value = 'True' WHERE (name = 'slewing');"

# mariadb -u alpaca -pdobri4 -D alpaca_scope -e "$query"


#get trckingrate


exit 0