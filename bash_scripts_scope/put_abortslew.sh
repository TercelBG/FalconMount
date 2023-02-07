#!/bin/bash



sudo python hardwarecontrol/abortslew.py


query="UPDATE properties SET value = 'False' WHERE (name = 'slewing');"
mariadb -u alpaca -pdobri4 -D alpaca_scope -e "$query"



#get trckingrate


exit 0