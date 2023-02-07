#!/bin/bash

#start the pigio demon
/home/alex/startgpiod.sh

echo "last value type is: $1"
echo "last value is: $2"
echo "Parameter 1 name is: $3"
echo "Parameter 1 type is: $4"
echo "Parameter 1 value is: $5"

query="UPDATE properties SET value = 'False' WHERE (name = 'atpark');"
mariadb -u alpaca -pdobri4 -D alpaca_scope -e "$query"

exit 0