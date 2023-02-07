#!/bin/bash

#start the pigio demon

echo "Setting Tracking rate impusts are:"
echo "last value type is: $1"
echo "last value is: $2"
echo "Parameter 1 name is: $3"
echo "Parameter 1 type is: $4"
echo "Parameter 1 value is: $5"


echo "Generated qeury is: "

query="UPDATE properties SET value = '$5' WHERE (name = 'trackingrate');"
mariadb -u alpaca -pdobri4 -D alpaca_scope -e "$query"
echo $query
exit 0