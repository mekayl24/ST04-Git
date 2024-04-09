
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import math
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import serial
import time
import matplotlib.animation as animation
import RPi.GPIO as GPIO


#Initialization


gpio_pin = 23

GPIO.setmode(GPIO.BCM)
GPIO.setup(gpio_pin, GPIO.IN, pull_up_down= GPIO.PUD_UP)

TimeStamps = [0]
sensor_change = [1]
initial_time = time.time()



def animate(frames): #can probably take the frames part out?

    TimeStamps = []


    while True:

        gpio_data = GPIO.input(gpio_pin)
        
        if gpio_data == 0 and sensor_change[-1] != 0:
            timestamp = time.time() - initial_time
            TimeStamps.append(timestamp)
            print("Timestamp: ",timestamp)
            sensor_change.append(0)
            #print(sensor_change)
        if gpio_data == 1:
            sensor_change.append(1)



animate(frames = None)
