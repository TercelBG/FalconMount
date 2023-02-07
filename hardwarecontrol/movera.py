import pigpio
import sys
import mariadb
import subprocess
arg1 = float(sys.argv[1])

DIR1 = 14     # Direction GPIO Pin
DIR2 = 15    # Step GPIO Pin
STEP1 = 18 # microstep selector 1
STEP2 = 23 # microstep selector 2
EN1 = 24 # enable M1
EN2 = 8 #  enable M2
LED = 20
MS1 = 21  #Multistepping M1


ANY_BUT = 0
DM1 = 1
DM2 = 0
pi = pigpio.pi()

# Set up pins as an output
pi.set_mode(DIR1, pigpio.OUTPUT)
pi.set_mode(DIR2, pigpio.OUTPUT)
pi.set_mode(STEP1, pigpio.ALT5)
pi.set_mode(STEP2, pigpio.OUTPUT)
pi.set_mode(EN1, pigpio.OUTPUT)
pi.set_mode(EN2, pigpio.OUTPUT)
pi.set_mode(LED, pigpio.OUTPUT)
pi.set_mode(MS1, pigpio.OUTPUT)

arg1 = float(sys.argv[1])
if arg1 == 0:
    pi.write(EN1,1)
    pi.hardware_PWM(18, 0 , 500000)
    pi.set_mode(STEP1, pigpio.OUTPUT)
    
    cnx_scope = mariadb.connect(user='alpaca', password='dobri4',
    host='192.168.1.21',
    database='alpaca_scope')
    cursor = cnx_scope.cursor()
    query = "update properties set value = 'False'   where name = 'slewing'"
    query2 = "update properties set value = '0'   where name = 'rightascensionrate'"
    query3 = "SELECT value FROM properties where name in ('tracking','trackingrate')"

    cursor.execute(query)
    cursor.execute(query2)
    cursor.execute(query3)
    value_row = cursor.fetchall()
    if value_row[0][0] == 'True':
        subprocess.call(['python','hardwarecontrol/start_tracking.py', value_row[1][0]])
    cursor.close()
    cnx_scope.commit()
    cnx_scope.close()

    subprocess.call(['python','hardwarecontrol/start_tracking.py'])
else:
    if arg1 > 0 :
        pi.write(DIR1,1)
    else: 
        pi.write(DIR1,0)

    speed =  abs (round(arg1*213333))


    # Set duty cycle and frequency
    #pi.set_PWM_dutycycle(STEP1, 128)  # PWM 1/2 On 1/2 Off
    #pi.set_PWM_frequency(STEP1, 2560)  # 500 pulses per second
    pi.write(EN1,0)

    pi.write(MS1,1)
    pi.hardware_PWM(18, speed , 500000)


    cnx_scope = mariadb.connect(user='alpaca', password='dobri4',
    host='192.168.1.21',
    database='alpaca_scope')
    cursor = cnx_scope.cursor()
    query = "update properties set value = '"+sys.argv[1]+"'   where name = 'rightascensionrate'"
    cursor.execute(query)
    cursor.close()
    cnx_scope.commit()
    cnx_scope.close()

# pi.write(DIR1,0)
# pi.write(DIR2,0)
# pi.write(EN1,0)
# pi.write(EN2,0)
# pi.write(MS1,1)
