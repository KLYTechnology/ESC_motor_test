#!/usr/bin/env python

#!/usr/bin/env python

## this script depends on PCA9685.py, so be sure to re-install PCA9685.py
## if you have changed anything in that script

from __future__ import division
import os  
import time  
import Adafruit_PCA9685

import thread

# frequency of ESC AIR 20A
ESC_FREQUENCY = 50

# ESC's are connected to 8, 9, 10, 11 four channels
ESC_ONE = 8
ESC_TWO = 9
ESC_THREE = 10
ESC_FOUR = 11   

# initialize pwm in PCA9685
pwm = Adafruit_PCA9685.PCA9685(address=0x44, busnum=0)
pwm.set_pwm_freq(ESC_FREQUENCY)

MAX_PWM_MOT = 2000
MIN_PWM_MOT = 1000

servo_min = int(1000.0*ESC_FREQUENCY*4096//1000000.0)  # Min pulse length out of 4096, 1000us in 60Hz
servo_max = 2*servo_min  # Max pulse length out of 4096, 2000us in 60Hz

def manual_drive(): #You will use this function to program your ESC if required
	print "You have selected manual option so give a value between 0 and you max value"    
	while True:
		inp = raw_input()
		if inp == "stop":
			stop()
			break
		elif inp == "control":
			control()
			break
		elif inp == "arm":
			arm()
			break
		else:
			pwm.set_ESC_pwm(ESC_ONE, inp, ESC_FREQUENCY)

def calibrate():   #This is the auto calibration procedure of a normal ESC
	pwm.set_ESC_pwm(ESC_ONE, 0, ESC_FREQUENCY)
	pwm.set_ESC_pwm(ESC_TWO, 0, ESC_FREQUENCY)
	pwm.set_ESC_pwm(ESC_THREE, 0, ESC_FREQUENCY)
	pwm.set_ESC_pwm(ESC_FOUR, 0, ESC_FREQUENCY)
	print("Disconnect the battery and press Enter")
	inp = raw_input()
	if inp == '':
		pwm.set_ESC_pwm(ESC_ONE, MAX_PWM_MOT, ESC_FREQUENCY)
		pwm.set_ESC_pwm(ESC_TWO, MAX_PWM_MOT, ESC_FREQUENCY)
		pwm.set_ESC_pwm(ESC_THREE, MAX_PWM_MOT, ESC_FREQUENCY)
		pwm.set_ESC_pwm(ESC_FOUR, MAX_PWM_MOT, ESC_FREQUENCY)
		print("Connect the battery NOW.. you will here two beeps, then wait for a gradual falling tone then press Enter")
		inp = raw_input()
		if inp == '':            
			pwm.set_ESC_pwm(ESC_ONE, MIN_PWM_MOT, ESC_FREQUENCY)
			pwm.set_ESC_pwm(ESC_TWO, MIN_PWM_MOT, ESC_FREQUENCY)
			pwm.set_ESC_pwm(ESC_THREE, MIN_PWM_MOT, ESC_FREQUENCY)
			pwm.set_ESC_pwm(ESC_FOUR, MIN_PWM_MOT, ESC_FREQUENCY)
			print "Wierd eh! Special tone"
			time.sleep(3)
			print "Wait for it ...."
			time.sleep (2)
			print "Im working on it, DONT WORRY JUST WAIT....."
			pwm.set_ESC_pwm(ESC_ONE, 0, ESC_FREQUENCY)
			pwm.set_ESC_pwm(ESC_TWO, 0, ESC_FREQUENCY)
			pwm.set_ESC_pwm(ESC_THREE, 0, ESC_FREQUENCY)
			pwm.set_ESC_pwm(ESC_FOUR, 0, ESC_FREQUENCY)
			time.sleep(1)
			print "Arming ESC now..."
			pwm.set_ESC_pwm(ESC_ONE, MIN_PWM_MOT, ESC_FREQUENCY)
			pwm.set_ESC_pwm(ESC_TWO, MIN_PWM_MOT, ESC_FREQUENCY)
			pwm.set_ESC_pwm(ESC_THREE, MIN_PWM_MOT, ESC_FREQUENCY)
			pwm.set_ESC_pwm(ESC_FOUR, MIN_PWM_MOT, ESC_FREQUENCY)
			time.sleep(1)
			print "See.... uhhhhh"
			control() # You can change this to any other function you want

def control(): 
	print "I'm Starting the motor, I hope its calibrated and armed, if not restart by giving 'x'"
	speed = 1300    # change your speed if you want to.... it should be between 700 - 2000
	print "Controls - a to decrease speed & d to increase speed OR q to decrease a lot of speed & e to increase a lot of speed"
	while True:
		pwm.set_ESC_pwm(ESC_ONE, speed, ESC_FREQUENCY)
		pwm.set_ESC_pwm(ESC_TWO, speed, ESC_FREQUENCY)
		pwm.set_ESC_pwm(ESC_THREE, speed, ESC_FREQUENCY)
		pwm.set_ESC_pwm(ESC_FOUR, speed, ESC_FREQUENCY)
		inp = raw_input()
		
		#~ ## for driving servo motors, comment if necessary
		#~ pwm.set_pwm(0, 0, servo_min)
		#~ pwm.set_pwm(1, 0, servo_min)
		#~ time.sleep(0.5)
		#~ pwm.set_pwm(0, 0, servo_max)
		#~ pwm.set_pwm(1, 0, servo_max)
		#~ time.sleep(0.5)

		if inp == "q":
			speed -= 100    # decrementing the speed like hell
			print "speed = %d" % speed
		elif inp == "e":    
			speed += 100    # incrementing the speed like hell
			print "speed = %d" % speed
		elif inp == "d":
			speed += 10     # incrementing the speed 
			print "speed = %d" % speed
		elif inp == "a":
			speed -= 10     # decrementing the speed
			print "speed = %d" % speed
		elif inp == "stop":
			stop()          #going for the stop function
			break
		elif inp == "manual":
			manual_drive()
			break
		elif inp == "arm":
			arm()
			break
		elif inp == "stopProgram":
			stopProgram()
			break
		else:
			print "WHAT DID I SAID!! Press a,q,d or e"

def arm(): #This is the arming procedure of an ESC 
	print "Connect the battery and press Enter"
	inp = raw_input()    
	if inp == '':
		pwm.set_ESC_pwm(ESC_ONE, 0, ESC_FREQUENCY)
		pwm.set_ESC_pwm(ESC_TWO, 0, ESC_FREQUENCY)
		pwm.set_ESC_pwm(ESC_THREE, 0, ESC_FREQUENCY)
		pwm.set_ESC_pwm(ESC_FOUR, 0, ESC_FREQUENCY)
		time.sleep(1)
		#~ pwm.set_ESC_pwm(ESC_ONE, MAX_PWM_MOT, ESC_FREQUENCY)
		#~ time.sleep(1)
		pwm.set_ESC_pwm(ESC_ONE, MIN_PWM_MOT, ESC_FREQUENCY)
		pwm.set_ESC_pwm(ESC_TWO, MIN_PWM_MOT, ESC_FREQUENCY)
		pwm.set_ESC_pwm(ESC_THREE, MIN_PWM_MOT, ESC_FREQUENCY)
		pwm.set_ESC_pwm(ESC_FOUR, MIN_PWM_MOT, ESC_FREQUENCY)
		time.sleep(1)
		control() 

def stop(): #This will stop every action your Pi is performing for ESC ofcourse.
	pwm.set_ESC_pwm(ESC_ONE, 0, ESC_FREQUENCY)
	pwm.set_ESC_pwm(ESC_TWO, 0, ESC_FREQUENCY)
	pwm.set_ESC_pwm(ESC_THREE, 0, ESC_FREQUENCY)
	pwm.set_ESC_pwm(ESC_FOUR, 0, ESC_FREQUENCY)
	commandESC()
	
def stopProgram():
	pwm.set_ESC_pwm(ESC_ONE, 0, ESC_FREQUENCY)
	pwm.set_ESC_pwm(ESC_TWO, 0, ESC_FREQUENCY)
	pwm.set_ESC_pwm(ESC_THREE, 0, ESC_FREQUENCY)
	pwm.set_ESC_pwm(ESC_FOUR, 0, ESC_FREQUENCY)
	pwm.set_pwm(0, 0, 0)
	pwm.set_pwm(1, 0, 0)
	
def commandServo():
	print('Moving servo on channel 0, press Ctrl-C to quit...')
	while True:
		# Move servo on channel O between extremes.
		pwm.set_pwm(0, 0, servo_min)
		pwm.set_pwm(1, 0, servo_min)
		time.sleep(1)
		pwm.set_pwm(0, 0, servo_max)
		pwm.set_pwm(1, 0, servo_max)
		time.sleep(1)

def commandESC():
	inp = raw_input()
	if inp == "manual":
		manual_drive()
	elif inp == "calibrate":
		calibrate()
	elif inp == "arm":
		arm()
	elif inp == "control":
		control()
	elif inp == "stop":
		stop()
	elif inp == "stopProgram":
		stopProgram()
	else:
		print "Thank You for not following the things I'm saying... now you gotta restart the program STUPID!!"

#This is the start of the program actually, to start the function it needs to be initialized before calling... stupid python.
thread.start_new_thread(commandServo, ()) 

if __name__=="__main__":
	commandESC()
	
	
	
	
	
	
