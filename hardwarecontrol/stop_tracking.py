from time import sleep
import pigpio



# 14,15,18,23,24,8,7,1,12,16,20,21

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

# Set up pins as an output
pi.set_mode(DIR1, pigpio.OUTPUT)
pi.set_mode(DIR2, pigpio.OUTPUT)
pi.set_mode(STEP1, pigpio.ALT5)
pi.set_mode(STEP2, pigpio.OUTPUT)
pi.set_mode(EN1, pigpio.OUTPUT)
pi.set_mode(EN2, pigpio.OUTPUT)
pi.set_mode(LED, pigpio.OUTPUT)
pi.set_mode(MS1, pigpio.OUTPUT)

pi.write(DIR1,0)
pi.hardware_PWM(18, 0 , 0)

pi.set_mode(STEP1, pigpio.OUTPUT)
pi.write(EN1,1)
pi.write(EN2,1)
# pi.write(DIR1,0)
# pi.write(DIR2,0)
# pi.write(EN1,0)
# pi.write(EN2,0)
# pi.write(MS1,1)
