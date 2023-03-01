from time import sleep
import pigpio
import sys
import mariadb
import threading

def move_ra(speed_ra,speed_dec, time_ra, time_dec, dir_ra, dir_dec, tracking, newra  ,newdec ) :
    # 14,15,18,23,24,8,7,1,12,16,20,21
    DIR1 = 14     # Direction GPIO Pin
    DIR2 = 15    # Step GPIO Pin
    STEP1 = 18 # microstep selector 1
    STEP2 = 23 # microstep selector 2
    EN1 = 24 # enable M1
    EN2 = 8 #  enable M2
    LED = 20
    MS1 = 21  #Multistepping M1
    DM1 = 1
    DM2 = 0
    pi = pigpio.pi()
    pi.set_mode(DIR1, pigpio.OUTPUT)
    pi.set_mode(EN1, pigpio.OUTPUT)
    pi.set_mode(LED, pigpio.OUTPUT)
    pi.write(DIR1,dir_ra)
    pi.write(EN1,0)
    pi.write(MS1,1)
    pi.hardware_PWM(STEP1, speed_ra , 500000)
    sleep(time_ra)

    if tracking == 'True':
        pi.hardware_PWM(STEP1, 891 , 500000)
    else:
        pi.set_mode(STEP1, pigpio.OUTPUT)
        pi.write(EN1,1)

    m2_cnx_scope = mariadb.connect(user='alpaca', password='dobri4',
                                    host='192.168.1.21',
                                    database='alpaca_scope')
    m2_cursor = m2_cnx_scope.cursor()
    query = "update properties set value = '"+str(newra)+"' where name = 'rightascension'"
    print (query)
    m2_cursor.execute(query)
    m2_cnx_scope.commit()
    m2_cursor.close()
    m2_cnx_scope.close()



    pi.set_mode(LED, pigpio.OUTPUT)
    pi.write(DIR2,dir_dec)
    pi.write(EN2,0)
    pi.write(LED,1)
    pi.set_PWM_dutycycle(STEP2, 128)
    pi.set_PWM_frequency(STEP2, speed_dec)
    sleep(time_dec)
    pi.set_PWM_dutycycle(STEP2, 0)
    pi.set_PWM_frequency(STEP2, 0)
    m2_cnx_scope = mariadb.connect(user='alpaca', password='dobri4',
                                    host='192.168.1.21',
                                    database='alpaca_scope')
    m2_cursor = m2_cnx_scope.cursor()
    query = "update properties set value = 'False' where name = 'slewing'"
    print (query)
    m2_cursor.execute(query)
    query = "update properties set value = '"+str(newdec)+"' where name = 'declination'"
    print (query)
    m2_cursor.execute(query)
    m2_cnx_scope.commit()
    m2_cursor.close()
    m2_cnx_scope.close()

print ("oldra is: ")
print(sys.argv[1])
print ("olddec is: ")
print(sys.argv[2])
print ("newra is: ")
print(sys.argv[3])
print ("oldra is: ")
print(sys.argv[4])
print ("tracking is: ")
print(sys.argv[5])

oldra = float(sys.argv[1])
olddec = float(sys.argv[2])
newra = float(sys.argv[3])
newdec = float(sys.argv[4])
tracking = str(sys.argv[5])

print(oldra)
print(olddec)
print(newra)
print(newdec)

rarate=0.5
decrate=1

print('hours to move')
to_move_ra=newra-oldra
print(to_move_ra)
if to_move_ra > 12:
    to_move_ra = to_move_ra-24
elif  to_move_ra < -12:
    to_move_ra = to_move_ra+24

if to_move_ra > 0 :
    dir_ra=1
else: 
    dir_ra=0
print('speed')
to_move_ra_deg=to_move_ra*15
speed_ra = abs(round(rarate*213333.333))
print('speed_ra')
time_ra = abs(to_move_ra_deg/rarate)
print('time')
print(time_ra)

to_move_dec=newdec-olddec

if to_move_dec > 0 :
    dir_dec=0
else: 
    dir_dec=1

speed_dec = abs(round(decrate*444.4444))
time_dec = abs((to_move_dec)/decrate)


thread_ra = threading.Thread(target=move_ra, args=(speed_ra,speed_dec, time_ra, time_dec, dir_ra, dir_dec, tracking, newra  ,newdec ))
thread_ra.start()
#thread_dec = threading.Thread(target=move_dec , args=(speed_dec, time_dec, dir_dec, newdec))
#thread_dec.start()