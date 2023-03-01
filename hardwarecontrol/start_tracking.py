import pigpio
import sys
import mariadb

trackingrate=str(sys.argv[1])
DIR1 = 14     # Direction GPIO Pin
STEP1 = 18 # microstep selector 1
EN1 = 24 # enable M1
LED = 20
MS1 = 21  #Multistepping M1
print ('start tracking at setting tracking rate')
print (trackingrate)

pi = pigpio.pi()

# Set up pins as an output
pi.set_mode(DIR1, pigpio.OUTPUT)
pi.set_mode(STEP1, pigpio.ALT5)
pi.set_mode(EN1, pigpio.OUTPUT)
pi.set_mode(LED, pigpio.OUTPUT)
pi.set_mode(MS1, pigpio.OUTPUT)

print ('iftest')
print (trackingrate)
print (trackingrate == '0')
print (trackingrate == '1')
print (trackingrate == '3')
if trackingrate == '0':
    speed=891
    rate=15.041
elif trackingrate == '1':
    speed=870
    rate=14.685
elif trackingrate == '2':
    speed=888
    rate=14.685  
elif trackingrate == '3':
    speed=891   
    rate=15.0369
else:
    speed=891
cnx_scope = mariadb.connect(user='alpaca', password='dobri4',
host='192.168.1.21',
database='alpaca_scope')
cursor = cnx_scope.cursor()
query = "update properties set value = '"+str(rate)+"'   where name = 'rightascensionrate'"
cursor.execute(query)
query2 = "update properties set value = 'True'   where name = 'tracking'"
cursor.execute(query2)
cursor.close()
cnx_scope.commit()
cnx_scope.close()
# Set duty cycle and frequency
#pi.set_PWM_dutycycle(STEP1, 128)  # PWM 1/2 On 1/2 Off
#pi.set_PWM_frequency(STEP1, 2560)  # 500 pulses per second
pi.write(EN1,0)
pi.write(MS1,1)
pi.write(DIR1,0)
pi.hardware_PWM(18, speed , 500000)
print ('start tracking at setting tracking rate')
print (trackingrate)
# pi.write(DIR1,0)
# pi.write(DIR2,0)
# pi.write(EN1,0)
# pi.write(EN2,0)
# pi.write(MS1,1)
