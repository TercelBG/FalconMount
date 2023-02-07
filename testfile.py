import mysql.connector

cnx = mysql.connector.connect(user='alpaca', password='dobri4',
                              host='192.168.1.21',
                              database='alpaca_camera')

cursor = cnx.cursor()

query = "SELECT * FROM properties"
cursor.execute(query)

results = cursor.fetchall()

for row in results:
    print(row)

    cursor.close()
cnx.close()