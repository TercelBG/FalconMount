#!/bin/bash



echo "last value type is: $1"
echo "last value is: $2"
echo "Parameter 1 name is: $3"
echo "Parameter 1 type is: $4"
echo "Parameter 1 value is: $5"

if [ "$5" == "True" ]; then
    query="select value  from properties  WHERE (name = 'trackingrate');"
    trackingrate=$(mariadb -u alpaca -pdobri4 -D alpaca_scope -e "$query")
    echo "tracking rate from SQL is $trackingrate" 
    python3 hardwarecontrol/start_tracking.py "$trackingrate"
else
    python3 hardwarecontrol/stop_tracking.py
fi

query="UPDATE properties SET value = '$5' WHERE (name = 'tracking');"
echo "Putting tracking to: $5"
echo $query
mariadb -u alpaca -pdobri4 -D alpaca_scope -e "$query"


#get trckingrate


exit 0