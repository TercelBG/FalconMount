#!/bin/bash




echo "last value type is: $1"
echo "last value is: $2"
echo "Parameter 1 name is: $3"
echo "Parameter 1 type is: $4"
echo "Parameter 1 value is: $5"

query="UPDATE properties SET value = '$5' WHERE (name = 'connected');"

echo $query

# Run the query using the mysql command-line client
mariadb -u alpaca -pdobri4 -D alpaca_camera -e "$query"
exit 0