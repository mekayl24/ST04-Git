import math
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from mathFunctionsPi import process_file, timeToDw, getDw, getInertia, getK, getDragPower, getAppliedPower, getsmoothedDt


import time
import RPi.GPIO as GPIO

# Initializations

#did this transfer over? fuck ye it did
gpio_pin = 23
GPIO.setmode(GPIO.BCM)
GPIO.setup(gpio_pin, GPIO.IN, pull_up_down = GPIO.PUD_UP)





def get_sensor_data():
    return GPIO.input(gpio_pin)




def update_data():
    gpio_data = get_sensor_data()
    
    if gpio_data == 0 and sensor_change[-1] != 0:
        timestamp = time.time() - initial_time
        
        TimeStamps.append(timestamp)
        sensor_change.append(0)
    if gpio_data ==1:
        sensor_change.append(1)
        #print("Not changing: ", sensor_change)
        
        
def animate(frame):
    
    update_data()
    
    
    dt = getsmoothedDt(TimeStamps)
    freq, angVel, RPMvalues = timeToDw(TimeStamps, dt)
    dw, angAccel = getDw(dt,angVel)
    inertia = getInertia(1.5, 0.3302)
    k = getK(angVel,angAccel,inertia)
    dragPow, dragTor = getDragPower(angVel, k)
    appliedPower, appliedTorque = getAppliedPower(dragTor, inertia, angAccel, angVel)
    
    if len(TimeStamps) >= 3:
        newTimeStamps = TimeStamps[2:]
        xandy.set_data(newTimeStamps, appliedPower)
        ax.relim()
        ax.autoscale_view()
    
    #plt.draw()
    #plt.pause(0.0001)
    return xandy



# Initialize variables and plot
TimeStamps = []
sensor_change = [1]
initial_time = time.time()


fig, ax = plt.subplots()
xandy, = ax.plot([], [], lw=2)
plt.title('Real-time Applied Power Plot')
plt.xlabel('Timestamp')
plt.ylabel('Applied Power')
plt.show(block=False)



# Start plotting animation
ani = FuncAnimation(fig, animate, frames=None, init_func = update_data, interval=100, save_count=10)
plt.show()






###This is code for trying to animate with the raspberry pi, wont work on desktop


# def animate(frames):

#     TimeStamps = []


#     while True:


#         #line = (ser.readline().decode().strip())

#         gpio_data = GPIO.input(gpio_pin)
        
#         if gpio_data == 0 and sensor_change[-1] != 0:
#             timestamp = time.time() - initial_time
#             TimeStamps.append(timestamp)
#             print("Timestamp: ",timestamp)
#             sensor_change.append(0)
#             #print(sensor_change)
#         if gpio_data == 1:
#             sensor_change.append(1)
#         #time.sleep(0.1)


#         #timeValue = float(line)
#         #TimeStamps.append(timeValue)

#         dt, freq, angVel, RPMvalues = timeToDw(TimeStamps)
#         dw, angAccel = getDw(dt,angVel)
#         inertia =(getInertia(1.5, 0.3302))
#         k = getK(angVel,angAccel,inertia)
#         dragPow, dragTor = getDragPower(angVel, k)
#         appliedPower, appliedTorque = getAppliedPower(dragTor, inertia, angAccel, angVel)
#         if len(TimeStamps)>= 3:
#             newTimeStamps = TimeStamps[2:]
#             #print("Time:", newTimeStamps)
#             #print("Power: ", appliedPower)
#             xandy.set_data(newTimeStamps,appliedPower)
#             ax.relim()
#             ax.autoscale_view()
#         plt.draw()
#         #plt.pause(0.0001)
#         #return xandy
        
# def getSensorData():
#     gpio_pin = 23

#     GPIO.setmode(GPIO.BCM)
#     GPIO.setup(gpio_pin, GPIO.IN, pull_up_down= GPIO.PUD_UP)


 
        
#     gpio_data = GPIO.input(gpio_pin)

#     print("Data: ", gpio_data)
        
#     time.sleep(1)
        
        


#ser = serial.Serial('COM5', 9600)

# gpio_pin = 23

# GPIO.setmode(GPIO.BCM)
# GPIO.setup(gpio_pin, GPIO.IN, pull_up_down= GPIO.PUD_UP)

# TimeStamps = [0]
# sensor_change = [1]
# initial_time = time.time()

# x_data = []
# y_data = []
# fig, ax = plt.subplots()
# xandy, = ax.plot([], [], lw=2)

# plt.title('Real-time Applied Power Plot')
# plt.xlabel('Timestamp')
# plt.ylabel('Applied Power')

# plt.show(block=False)



# animate(frames = None)

#ani = FuncAnimation(fig, animate, frames=None ,interval = 100, save_count= 1000)

