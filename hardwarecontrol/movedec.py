from time import sleep
import pigpio
import sys
import mariadb
# 14,15,18,23,24,8,7,1,12,16,20,21


cnx_scope = mariadb.connect(user='alpaca', password='dobri4',
host='192.168.1.21',
database='alpaca_scope')
cursor = cnx_scope.cursor()
query = "update properties set value = '"+sys.argv[1]+"'   where name = 'declinationrate'"
cursor.execute(query)
cursor.close()
cnx_scope.commit()
cnx_scope.close()


DIR1 = 14     # Direction GPIO Pin
DIR2 = 15    # Step GPIO Pin
STEP1 = 18 # microstep selector 1
STEP2 = 23 # microstep selector 2
EN1 = 24 # enable M1
EN2 = 8 #  enable M2

LED = 20
MS1 = 21  #Multistepping M1




F1 = 200
F2 = 0

ANY_BUT = 0
DM1 = 1
DM2 = 0
pi = pigpio.pi()


pi.set_mode(DIR2, pigpio.OUTPUT)
pi.set_mode(STEP2, pigpio.OUTPUT)
pi.set_mode(EN2, pigpio.OUTPUT)
pi.set_mode(LED, pigpio.OUTPUT)



# Set duty cycle and frequency
#pi.set_PWM_dutycycle(STEP1, 128)  # PWM 1/2 On 1/2 Off
#pi.set_PWM_frequency(STEP1, 2560)  # 500 pulses per second
pi.write(DIR2,1)
pi.write(EN2,0)
arg1 = float(sys.argv[1])
if arg1 == 0:
    pi.set_PWM_dutycycle(STEP2, 0)
    pi.set_PWM_frequency(STEP2, 0)
    pi.write(EN2,1)

    cnx_scope = mariadb.connect(user='alpaca', password='dobri4',
    host='192.168.1.21',
    database='alpaca_scope')
    cursor = cnx_scope.cursor()
    query = "update properties set value = 'False'   where name = 'slewing'"
    cursor.execute(query)
    cursor.close()
    cnx_scope.commit()
    cnx_scope.close()

else:
    speed=round(abs(arg1)*444/60/60)
    if arg1 > 0 :
        pi.write(DIR2,0)
        pi.set_PWM_dutycycle(STEP2, 128)
        pi.set_PWM_frequency(STEP2, speed)
    else : 
        pi.write(DIR2,1)
        pi.set_PWM_dutycycle(STEP2, 128)
        pi.set_PWM_frequency(STEP2, speed)




