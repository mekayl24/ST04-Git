
import math
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
#from mathFunctions import process_file, timeToDw, getDw, getInertia, getK, getDragPower, getAppliedPower, getsmoothedDt
import serial
import threading
import queue
import time


def timeToDw(TimeStamps):
    #Initializing empty lists for parameters
    dt = []
    freq = []
    angVel = []
    RPMvalues = []
    for i in range(len(TimeStamps)-1):
        newStamp = TimeStamps[i+1] - TimeStamps[i] #Calculating all values
        frequency = 1/newStamp
        angularVelocity = 2*math.pi*frequency
        RPM = angularVelocity * (60/ (2*math.pi))


        dt.append(newStamp)         #Adding values to lists
        freq.append(frequency)
        angVel.append(angularVelocity)
        RPMvalues.append(RPM)
    return dt, freq, angVel, RPMvalues
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
    k = [0.00027]
    for i in range(len(angVel) -1):
        if angAccel[i] < 0:
            kVal = (-inertia*angAccel[i])/(angVel[i+1])**2
        else:
            kVal = 0.00027
        k.append(kVal)
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



def read_serial_data(ser, q):
    while True:
        line = ser.readline().decode().strip()
        timeValue = float(line)
        print(timeValue)
        q.put(timeValue)

def update_plot(frame):
    while not q.empty():
        timeValue = q.get()
        TimeStamps.append(timeValue)
        dt, freq, angVel, RPMvalues = timeToDw(TimeStamps)
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
    return xandy

# Initialize serial port
ser = serial.Serial('COM7', 9600)

# Initialize variables and plot
TimeStamps = []
x_data = []
y_data = []
fig, ax = plt.subplots()
xandy, = ax.plot([], [], lw=2)
plt.title('Real-time Applied Power Plot')
plt.xlabel('Timestamp')
plt.ylabel('Applied Power')
plt.show(block=False)

# Create a queue to pass data between threads
q = queue.Queue()

# Start a thread to read serial data
serial_thread = threading.Thread(target=read_serial_data, args=(ser, q))
serial_thread.daemon = True
serial_thread.start()

# Start plotting animation
ani = FuncAnimation(fig, update_plot, frames=None, interval=100, save_count=10)
plt.show()


###This is code for trying to animate with the raspberry pi, wont work on desktop


# def animate(frames):

#     TimeStamps = []


#     while True:


#         line = (ser.readline().decode().strip())

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
        
        


#ser = serial.Serial('COM7', 9600)

# gpio_pin = 23

# GPIO.setmode(GPIO.BCM)
# GPIO.setup(gpio_pin, GPIO.IN, pull_up_down= GPIO.PUD_UP)

TimeStamps = [0]
sensor_change = [1]
initial_time = time.time()

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

