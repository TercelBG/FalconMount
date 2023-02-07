import pigpio
import sys

trackingrate=str(sys.argv[1])
DIR1 = 14     # Direction GPIO Pin
DIR2 = 15    # Step GPIO Pin
STEP1 = 18 # microstep selector 1
STEP2 = 23 # microstep selector 2
EN1 = 24 # enable M1
EN2 = 8 #  enable M2
LED = 20
MS1 = 21  #Multistepping M1
print ('start tracking at setting tracking rate')
print (trackingrate)

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


if trackingrate == '0':
    speed=891
elif trackingrate == '1':
    speed=1891
elif trackingrate == '2':
    speed=2891    
elif trackingrate == '3':
    speed=2891    
else:
    speed=891
# Set duty cycle and frequency
#pi.set_PWM_dutycycle(STEP1, 128)  # PWM 1/2 On 1/2 Off
#pi.set_PWM_frequency(STEP1, 2560)  # 500 pulses per second
pi.write(EN1,0)
pi.write(EN2,0)
pi.write(MS1,1)
pi.hardware_PWM(18, speed , 500000)

# pi.write(DIR1,0)
# pi.write(DIR2,0)
# pi.write(EN1,0)
# pi.write(EN2,0)
# pi.write(MS1,1)
