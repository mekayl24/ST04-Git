import threading
import math
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from mathFunctionsPi import process_file, timeToDw, getDw, getInertia, getK, getDragPower, getAppliedPower, getsmoothedDt
import time
import RPi.GPIO as GPIO
from moving_averagePi import moving_average
from scipy.signal import savgol_filter
# Initialize GPIO pin
gpio_pin = 23
GPIO.setmode(GPIO.BCM)
GPIO.setup(gpio_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Global variables
TimeStamps = []
sensor_change = [1]
initial_time = time.time()
appliedPower = [1]
dtTest = []
#max_power = 0.0

interval_start_time = initial_time 
# Lock for thread safety
lock = threading.Lock()



def get_sensor_data():
    return GPIO.input(gpio_pin)


def update_data():
    global TimeStamps, sensor_change, initial_time, appliedPower, interval_start_time, dt, dtTest
    
    while True:
        gpio_data = get_sensor_data()
        with lock:
            if gpio_data == 0 and sensor_change[-1] != 0:
                timestamp = time.time() - initial_time
                TimeStamps.append(timestamp)
                if len(TimeStamps) > 2:
                    
                    dtTest = (TimeStamps[-1] - TimeStamps[-2])
                    #print("TimeStamps: ", TimeStamps[-1])
                    #print("Dt: ", dtTest)
                
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

""" #un comment to do first plot

fig1, ax1 = plt.subplots()
xandy1, = ax1.plot([], [], lw=2)
ax1.set_title('Real-time Applied Power Plot')
ax1.set_xlabel('Timestamp')
ax1.set_ylabel('Applied Power')

"""

# Plot initialization for angular velocity
fig2, ax2 = plt.subplots()
xandy2, = ax2.plot([], [], lw=2)
ax2.set_title('Real-time Angular Velocity Plot')
ax2.set_xlabel('Timestamp')
ax2.set_ylabel('Angular Velocity')


#un comment to do third plot
# Plot initialization for angular acceleration
fig3, ax3 = plt.subplots()
xandy3, = ax3.plot([], [], lw=2)
ax3.set_title('Real-time Angular Acceleration Plot')
ax3.set_xlabel('Timestamp')
ax3.set_ylabel('Angular Acceleration')



#un comment to do t plot
# Plot initialization for timestamps
fig4, ax4 = plt.subplots()
xandy4, = ax4.plot([], [], lw=2)
ax4.set_title('Real-time Dt')
ax4.set_xlabel('Timestamp')
ax4.set_ylabel('Dt')



plt.show(block=False)

# Animation function
# Animation function for applied power
def animate_power(frame):
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
            newTimeStampsPwr = TimeStamps[2:]
            # Plot applied power
            xandy1.set_data(newTimeStampsPwr, appliedPower)
            ax1.relim()
            ax1.autoscale_view()
            ax1.set_xlim(newTimeStampsPwr[-1] - 5, newTimeStampsPwr[-1])
    
    return xandy1

# Animation function for angular velocity
def animate_velocity(frame):
    global TimeStamps, appliedPower
    
    with lock:
        dt = getsmoothedDt(TimeStamps)
        
        freq, angVel, RPMvalues = timeToDw(TimeStamps, dt)
        
        if len(TimeStamps) >= 2:
            newTimeStampsVel = TimeStamps[1:]
            # Plot angular velocity
            xandy2.set_data(newTimeStampsVel, angVel)
            ax2.relim()
            ax2.autoscale_view()
            ax2.set_xlim(newTimeStampsVel[-1] - 5, newTimeStampsVel[-1])
    
    return xandy2

# Animation function for angular acceleration
def animate_acceleration(frame):
    global TimeStamps, appliedPower
    
    with lock:
        dt = getsmoothedDt(TimeStamps)
        freq, angVel, RPMvalues = timeToDw(TimeStamps, dt)
        dw, angAccel = getDw(dt, angVel)
        
        if len(TimeStamps) >= 3:
            newTimeStampsAcc = TimeStamps[2:]
            # Plot angular acceleration
            xandy3.set_data(newTimeStampsAcc, angAccel)
            ax3.relim()
            ax3.autoscale_view()
            ax3.set_xlim(newTimeStampsAcc[-1] - 5, newTimeStampsAcc[-1])
    
    return xandy3

def animate_time(frame):
    global TimeStamps
    
    dt = []
    for i in range(len(TimeStamps)-1):
        diffT = TimeStamps[i+1] - TimeStamps[i]
        dt.append(diffT)
    
    with lock:
        if len(TimeStamps) >= 2:
            newTimeStamps = TimeStamps[1:]
            new_dt = dt
            #new_dt = moving_average(dt, 100)  # Use only available dt data
            
            # Update the maximum value of the last interval
            max_dt_interval = max(new_dt)
            
            # Plot timestamps
            xandy4.set_data(newTimeStamps, new_dt)
            
            # Auto-adjust Y-axis to the maximum value of the last interval
            ax4.relim()
            ax4.autoscale_view()
            
            # Set X-axis limit to show only the last 5 seconds
            ax4.set_xlim(newTimeStamps[-1] - 5, newTimeStamps[-1])
            
            # Set the maximum value of the y-axis to 0.3
            ax4.set_ylim(0, 0.3)
    
    return xandy4
"""def animate_time(frame):
    global TimeStamps
    
    dt = []
    for i in range(len(TimeStamps)-1):
        diffT = TimeStamps[i+1] - TimeStamps[i]
        dt.append(diffT)
    #print("Dt: ",dt)    
    with lock:
        #dt = getsmoothedDt(TimeStamps)
        if len(TimeStamps) >= 2:
            newTimeStamps = TimeStamps[1:]
            
            # Plot timestamps
            xandy4.set_data(newTimeStamps, dt)  # Use only available dt data
            ax4.relim()
            ax4.autoscale(axis='y') 
            ax4.set_xlim(newTimeStamps[-1] - 5, newTimeStamps[-1])
    
    return xandy4

"""

# Animation for applied power
#ani = FuncAnimation(fig1, animate_power, frames=None, interval=100, save_count=10)

# Animation for angular velocity
ani2 = FuncAnimation(fig2, animate_velocity, frames=None, interval=100, save_count=10)


# Animation for angular acceleration

ani3 = FuncAnimation(fig3, animate_acceleration, frames=None, interval=100, save_count=10)


ani4 = FuncAnimation(fig4, animate_time, frames=None, interval=100, save_count=10)

plt.show()

"""
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
            newTimeStampsPwr = TimeStamps[2:]
            newTimeStampsAcc = TimeStamps[2:]
            newTimeStampsVel = TimeStamps[1:]
            # Plot applied power
            xandy.set_data(newTimeStampsPwr, appliedPower)
            # Plot angular velocity
            xandy2.set_data(newTimeStampsVel, angVel)
            # Plot angular acceleration
            xandy3.set_data(newTimeStampsAcc, angAccel)
            
            for ax in [ax1, ax2, ax3]:
                ax.relim()
                ax.autoscale_view()
                ax.set_xlim(newTimeStampsPwr[-1] - 5, newTimeStampsPwr[-1])
    
            #ax.relim()
            #ax.autoscale_view()
            #ax.set_xlim(newTimeStampsPwr[-1] - 5, newTimeStampsPwr[-1])
            #ax.set_ylim(appliedPower[-1] - 5, appliedPower[-1])
    
    return xandy, xandy2, xandy3

# Plot initialization

fig, (ax1, ax2, ax3) = plt.subplots(3, 1, sharex=True)
xandy, = ax1.plot([], [], lw=2)
xandy2, = ax2.plot([], [], lw=2)
xandy3, = ax3.plot([], [], lw=2)

ax1.set_title('Real-time Applied Power Plot')
ax1.set_ylabel('Applied Power')
ax2.set_ylabel('Angular Velocity')
ax3.set_ylabel('Angular Acceleration')
ax3.set_xlabel('Timestamp')
"""
"""
#fig, ax = plt.subplots()
xandy, = ax.plot([], [], lw=2, label='Applied Power')
xandy2, = ax.plot([], [], lw=2, label='Angular Velocity')
xandy3, = ax.plot([], [], lw=2, label='Angular Acceleration')
plt.title('Real-time Data Plot')
plt.xlabel('Timestamp')
plt.ylabel('Value')
plt.legend()
plt.show(block=False)

# Animation
#ani = FuncAnimation(fig, animate, frames=None, interval=100, save_count=10)
#plt.show()
"""
