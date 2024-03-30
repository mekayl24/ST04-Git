
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import math
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import serial
import time
import matplotlib.animation as animation
from moving_averagePiGUI import moving_average
#import RPi.GPIO as GPIO






def process_file(file_path):
    # List to store the numbers from the txt file
    TimeStamps = []

    with open(file_path, 'r') as file:
        for line in file:
            
            timestamp = float(line.split(':')[1].strip())
            TimeStamps.append(timestamp)
            
            ## old method
            # Split the line into individual numbers and convert to float
            #line_numbers = [float(num) for num in line.split()]
            #TimeStamps.extend(line_numbers)  # Add numbers to list


    return TimeStamps



def getsmoothedDt(TimeStamps):
    dtraw = []
    for i in range(len(TimeStamps)-1):
        newStamp = TimeStamps[i+1] - TimeStamps[i] #Calculating all values
        dtraw.append(newStamp)  
    dt = moving_average(dtraw, 32)
    return dt
    
    

def timeToDw(TimeStamps, dt):
    #Initializing empty lists for parameters
    
    freq = []
    angVel = []
    RPMvalues = []
    for i in range(len(TimeStamps)-1):
        newStamp = dt[i] #Calculating all values
        frequency = (1/newStamp)/16
        angularVelocity = 2*math.pi*frequency
        RPM = angularVelocity * (60/ (2*math.pi))


                #Adding values to lists
        freq.append(frequency)
        angVel.append(angularVelocity)
        RPMvalues.append(RPM)
    return freq, angVel, RPMvalues
def getDw(dt,angVel):
    dw = []
    angAccel = []
    for i in range(len(angVel)-1):
        newVal = angVel[i+1] - angVel[i]
        accelValue = newVal / dt[i+1]

        dw.append(newVal)
        angAccel.append(accelValue)

    return dw, angAccel

def getInertia(mass,radius):
    inertia = 0.5*mass*(radius**2)
    return inertia

def getK(angVel,angAccel, inertia):
    k =[0.0002]
    kVal2 = 0.0002  #comment this line if using calculation line of code
    for i in range(len(angVel) -1):
        if angAccel[i] < 0:
            kVal = (-inertia*angAccel[i])/(angVel[i+1])**2
        else:
            kVal = 0.0002


        #k.append(kVal) # this line is for calculating the drag factor when declerating, and using constant value when accelerating

        k.append(kVal2)   # this line is for just using a constant value
    return k


def getDragPower(angVel,k):
    dragTor = []
    dragPower = []
    for i in range(len(angVel) - 1):
        dragTorVal = k[i] * (angVel[i])**2
        dragPwrVal = dragTorVal * angVel[i]
        dragTor.append(dragTorVal)
        dragPower.append(dragPwrVal)
    return dragPower, dragTor
def getAppliedPower(dragTor,inertia, angAccel, angVel):
    netTorque = []
    appliedTorque = []
    appliedPower = [0, ]

    for i in range(len(angAccel)- 1):

        if angAccel[i] > 0: #If accelerating, calculate applied power, if not, then value is 0

            netTorqueVal = inertia* angAccel[i]
            appTorVal = netTorqueVal + dragTor[i+1]
            appPowerVal = appTorVal*angVel[i+1]

            netTorque.append(netTorqueVal)
            appliedTorque.append(appTorVal)
            appliedPower.append(appPowerVal)
        else:

            appTorVal = 0
            appPowerVal = 0
            appliedTorque.append(appTorVal)
            appliedPower.append(appPowerVal)

    return appliedPower, appliedTorque






