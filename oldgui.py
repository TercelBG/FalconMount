from time import sleep
import pigpio
import os
from gpiozero import LED, Button
from guizero import App, Text, PushButton, Picture, Box
import subprocess


# 14,15,18,23,24,8,7,1,12,16,20,21

DIR1 = 14     # Direction GPIO Pin
DIR2 = 15    # Step GPIO Pin
STEP1 = 18 # microstep selector 1
STEP2 = 23 # microstep selector 2
EN1 = 24 # enable M1
EN2 = 8 #  enable M2

BUT1 = Button(7,bounce_time=None)
BUT2 = Button(1,bounce_time=None)
BUT3 = Button(12,bounce_time=None)
BUT4 = Button(16,bounce_time=None)
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




# Set duty cycle and frequency
#pi.set_PWM_dutycycle(STEP1, 128)  # PWM 1/2 On 1/2 Off
#pi.set_PWM_frequency(STEP1, 2560)  # 500 pulses per second
pi.hardware_PWM(18, 891 , 500000)
pi.set_PWM_dutycycle(STEP2, 0)  # PWM 1/2 On 1/2 Off
pi.set_PWM_frequency(STEP2, 0)  # 500 pulses per second

pi.write(DIR1,0)
pi.write(DIR2,0)
pi.write(EN1,0)
pi.write(EN2,0)
pi.write(MS1,1)

def POSITION():
    POSITION_TEXT = subprocess.check_output('/home/alex/getcurrposition2.sh' ,shell=True)
#    POSITION_TEXT=os.system('/home/alex/getcurrposition.sh')
    previewbox.value = "/mnt/photos/raspberry/tmp/position-ngc-rsz.png"
    previewtext.value = POSITION_TEXT


def FOCUS():
    subprocess.check_output('/home/alex/focussnap.sh' ,shell=True)
#    POSITION_TEXT=os.system('/home/alex/getcurrposition.sh')
    previewbox.value = "/mnt/photos/raspberry/tmp/position-rsz.png"
    #previewtext.value = POSITION_TEXT


def ON_EXIT():
    #if App.yesno("","Close", "Do you want to quit?"):
    GUI_APP.destroy()

    #pi.set_PWM_dutycycle(STEP1, 0)  # PWM off
    pi.hardware_PWM(18, 0, 500000)
    pi.set_PWM_dutycycle(STEP2, 0)
    pi.write(EN1,1)
    pi.write(EN2,1)
    pi.stop()

GUI_APP= App(title="Motion controla", width=1024, height=1024)

D1_TEXT = Text(GUI_APP,"First Motor Direction: ")
D2_TEXT = Text(GUI_APP,"Second Motor Direction: ")
F1_TEXT = Text(GUI_APP,"First Motor Speed: ")
F2_TEXT = Text(GUI_APP,"Second Motor Speed: ")


def BUT_CHANGE(SPEED,DIRECTION,MOTOR):
    DISPLAY_SPEEDS(SPEED,DIRECTION,MOTOR)
    if SPEED > 3000:
        pi.write(LED,1)
    else:
        pi.write(LED,0)

    if MOTOR==1:
        if SPEED > 3000:
            pi.write(DIR1,DIRECTION)
            SPEEDX = pi.get_PWM_frequency(STEP1)
            while SPEEDX <= SPEED:
                SPEEDX = int(SPEEDX*1.8)
               # print (SPEEDX)
                #pi.set_PWM_frequency(STEP1, SPEEDX)
                pi.hardware_PWM(18, SPEEDX, 500000)
                sleep(0.5)
            pi.hardware_PWM(18, SPEED, 500000)
        else:
            SPEEDX = pi.get_PWM_frequency(STEP1)
            pi.write(LED,0)
            while SPEEDX >= SPEED:
                SPEEDX = int(SPEEDX/1.8)
                #pi.set_PWM_frequency(STEP1, SPEEDX)
                pi.hardware_PWM(18, SPEEDX, 500000)
               # print (SPEEDX)
                sleep(0.5)
            pi.write(DIR1,DIRECTION)
            pi.hardware_PWM(18, SPEED, 500000)
    if MOTOR==2:
        if SPEED > 20:
            pi.write(LED,1)
            SPEEDX = pi.get_PWM_frequency(STEP2)
            pi.write(DIR2,DIRECTION)
            while SPEEDX <= SPEED:
                pi.set_PWM_frequency(STEP2, SPEEDX)
                SPEEDX = SPEEDX+200
                print (SPEEDX)
                sleep(0.5)
            pi.set_PWM_frequency(STEP2, SPEED)
        else:
            pi.write(LED,0)
            SPEEDX = pi.get_PWM_frequency(STEP2)
            print (SPEEDX)
            pi.write(DIR2,DIRECTION)
            while SPEEDX >= SPEED:
                pi.set_PWM_frequency(STEP2, SPEEDX)
                SPEEDX = SPEEDX-200
                print (SPEEDX)
                sleep(0.5)
            pi.set_PWM_frequency(STEP2, SPEED)
        if  SPEEDX <= 0:
            pi.set_PWM_dutycycle(STEP2, 0)
        else:
            pi.set_PWM_dutycycle(STEP2, 128)
    DISPLAY_SPEEDS(SPEED,DIRECTION,MOTOR)

def BUT1_PRESS():
    print("Button 1 was pushed!")
    BUT_CHANGE(160000,1,1)

def BUT1_RELEASE():
    print("Button 1 was released!")
    BUT_CHANGE(891,1,1)

def BUT2_PRESS():
    print("Button 2 was pushed!")
    BUT_CHANGE(160000,0,1)

def BUT2_RELEASE():
    print("Button 2 was released!")
    BUT_CHANGE(891,1,1)

def BUT3_PRESS():
    print("Button 3 was pushed!")
    BUT_CHANGE(500,0,2)

def BUT3_RELEASE():
    print("Button 3 was released!")
    BUT_CHANGE(0,0,2)

def BUT4_PRESS():
    print("Button 4 was pushed!")
    BUT_CHANGE(500,1,2)

def BUT4_RELEASE():
    print("Button 4 was released!")
    BUT_CHANGE(0,1,2)

BUT1.when_pressed = BUT1_PRESS
BUT1.when_released = BUT1_RELEASE
BUT2.when_pressed = BUT2_PRESS
BUT2.when_released = BUT2_RELEASE
BUT3.when_pressed = BUT3_PRESS
BUT3.when_released = BUT3_RELEASE
BUT4.when_pressed = BUT4_PRESS
BUT4.when_released = BUT4_RELEASE


def DISPLAY_SPEEDS(SPEED,DIRECTION,MOTOR):
    if MOTOR == 1:
        D1_TEXT.clear()
        D1_TEXT.append("First Motor Direction: ")
        D1_TEXT.append(DIRECTION)
        F1_TEXT.clear()
        F1_TEXT.append("First Motor Speed: ")
        F1_TEXT.append(pi.get_PWM_frequency(STEP1))
    else:
        D2_TEXT.clear()
        D2_TEXT.append("Second Motor Direction: ")
        D2_TEXT.append(DIRECTION)
        F2_TEXT.clear()
        F2_TEXT.append("Second Motor Speed: ")
        F2_TEXT.append(pi.get_PWM_frequency(STEP2))

box_ra = Box(GUI_APP,layout="grid")
box_dec = Box(GUI_APP,layout="grid")
box_preview = Box(GUI_APP,layout="grid")

button = PushButton(box_ra, command=BUT1_PRESS, text="RA+" , grid=[0,0])
button2 = PushButton(box_ra, command=BUT1_RELEASE,text="STOP RA+"  , grid=[1,0])

button = PushButton(box_ra, command=BUT2_PRESS, text="RA-", grid=[2,0])
button2 = PushButton(box_ra, command=BUT2_RELEASE, text="STOP RA-"  , grid=[3,0])

button = PushButton(box_dec, command=BUT3_PRESS, text="DEC+" , grid=[0,0] )
button2 = PushButton(box_dec, command=BUT3_RELEASE, text="STOP DEC+" , grid=[1,0] )

button = PushButton(box_dec, command=BUT4_PRESS, text="DEC-" , grid=[2,0])
button2 = PushButton(box_dec, command=BUT4_RELEASE, text="STOP DEC-" , grid=[3,0] )

position = PushButton(box_preview, command=POSITION, text="current position" ,grid=[0,0] )
position = PushButton(box_preview, command=FOCUS, text="Focus" ,grid=[1,0] )

previewbox = Picture(box_preview,grid=[0,1])
previewtext = Text(box_preview, grid=[1,1])
GUI_APP.when_closed = ON_EXIT
GUI_APP.display()

