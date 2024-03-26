import threading
import math
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from mathFunctionsPi import process_file, timeToDw, getDw, getInertia, getK, getDragPower, getAppliedPower, getsmoothedDt
import time
import RPi.GPIO as GPIO

# Initialize GPIO pin
gpio_pin = 23
GPIO.setmode(GPIO.BCM)
GPIO.setup(gpio_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Global variables
TimeStamps = []
sensor_change = [1]
initial_time = time.time()
#max_power = 0.0

interval_start_time = initial_time 
# Lock for thread safety
lock = threading.Lock()



def get_sensor_data():
    return GPIO.input(gpio_pin)


def update_data():
    global TimeStamps, sensor_change, initial_time, appliedPower, interval_start_time
    
    while True:
        gpio_data = get_sensor_data()
        with lock:
            if gpio_data == 0 and sensor_change[-1] != 0:
                timestamp = time.time() - initial_time
                TimeStamps.append(timestamp)
                print(TimeStamps[-1])
                sensor_change.append(0)
            elif gpio_data == 1:
                sensor_change.append(1)
        
        current_time = time.time()
        if current_time - interval_start_time >= 5:
            with lock:
                # Update max_power to the maximum power recorded in the previous 5-second interval
                max_power = max(appliedPower)
                # Update the start time of the current 5-second interval
                interval_start_time = current_time
        
        time.sleep(0.01)  # Adjust sleep time as needed

# Thread for updating data
update_thread = threading.Thread(target=update_data)
update_thread.daemon = True  # Daemonize the thread so it exits when the main program ends
update_thread.start()

# Animation function

def animate(frame):
    global TimeStamps, appliedPower
    
    with lock:
        dt = getsmoothedDt(TimeStamps)
        freq, angVel, RPMvalues = timeToDw(TimeStamps, dt)
        dw, angAccel = getDw(dt, angVel)
        inertia = getInertia(1.5, 0.3302)
        k = getK(angVel, angAccel, inertia)
        dragPow, dragTor = getDragPower(angVel, k)
        appliedPower, appliedTorque = getAppliedPower(dragTor, inertia, angAccel, angVel)
        
        if len(TimeStamps) >= 3:
            newTimeStamps = TimeStamps[2:]
            xandy.set_data(newTimeStamps, appliedPower)
            ax.relim()
            ax.autoscale_view()
            ax.set_xlim(newTimeStamps[-1] - 5, newTimeStamps[-1])
    
    return xandy

# Plot initialization
fig, ax = plt.subplots()
xandy, = ax.plot([], [], lw=2)
plt.title('Real-time Applied Power Plot')
plt.xlabel('Timestamp')
plt.ylabel('Applied Power')
plt.show(block=False)

# Animation
ani = FuncAnimation(fig, animate, frames=None, interval=100, save_count=10)
plt.show()


"""
def update_data():
    gpio_data = get_sensor_data()
    
    if gpio_data == 0 and sensor_change[-1] != 0:
        timestamp = time.time() - initial_time
        
        TimeStamps.append(timestamp)
        print(TimeStamps[-1])
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
        #print("Time:", newTimeStamps[-1])
        #print("Power: ", appliedPower[-1])
        ax.relim()
        ax.autoscale_view()
    
    #plt.draw()
    print(appliedPower[-1], TimeStamps)    
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
#plt.show(block=False)


# Start plotting animation
#ani = FuncAnimation(fig, animate, frames=None, init_func = update_data, interval=100, save_count=10)
#plt.show()



"""


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

