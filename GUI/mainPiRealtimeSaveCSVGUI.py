import threading
import math
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from mathFunctionsPi import process_file, timeToDw, getDw, getInertia, getK, getDragPower, getAppliedPower, getsmoothedDt
import time
import RPi.GPIO as GPIO
from moving_averagePi import moving_average
from scipy.signal import savgol_filter
from matplotlib.widgets import Button
import csv

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
lock = threading.Lock()
interval_start_time = initial_time



def get_sensor_data():
    return GPIO.input(gpio_pin)

def update_data():
    global TimeStamps, sensor_change, initial_time, appliedPower, dt, dtTest, interval_start_time, angVel, angAccel
    
    while True:
        gpio_data = get_sensor_data()
        with lock:
            if gpio_data == 0 and sensor_change[-1] != 0:
                timestamp = time.time() - initial_time
                TimeStamps.append(timestamp)
                if len(TimeStamps) > 2:
                    dtTest = (TimeStamps[-1] - TimeStamps[-2])
                sensor_change.append(0)
            elif gpio_data == 1:
                sensor_change.append(1)
        
        current_time = time.time()
        if current_time - interval_start_time >= 5:
            with lock:
                interval_start_time = current_time
        
        time.sleep(0.01)  

update_thread = threading.Thread(target=update_data)
update_thread.daemon = True
update_thread.start()

 #un comment to do first plot

fig1, ax1 = plt.subplots()
xandy1, = ax1.plot([], [], lw=2)
ax1.set_title('Real-time Applied Power Plot')
ax1.set_xlabel('Timestamp')
ax1.set_ylabel('Applied Power')



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


def animate_power(frame):
    global TimeStamps, appliedPower, angAccel
    
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
            xandy1.set_data(newTimeStampsPwr, appliedPower)
            ax1.relim()
            ax1.autoscale_view()

    return xandy1

def animate_velocity(frame):
    global TimeStamps, appliedPower, angVel
    
    with lock:
        dt = getsmoothedDt(TimeStamps)
        freq, angVel, RPMvalues = timeToDw(TimeStamps, dt)
        if len(TimeStamps) >= 2:
            newTimeStampsVel = TimeStamps[1:]
            if len(angVel) >= 5:
                angVel_smoothed = savgol_filter(angVel, window_length=5, polyorder=3)
            else:
                angVel_smoothed = angVel
            xandy2.set_data(newTimeStampsVel, angVel_smoothed)
            ax2.relim()
            ax2.autoscale_view()

    return xandy2

def animate_acceleration(frame):
    global TimeStamps, appliedPower, angAccel
    
    with lock:
        dt = getsmoothedDt(TimeStamps)
        freq, angVel, RPMvalues = timeToDw(TimeStamps, dt)
        dw, angAccel = getDw(dt, angVel)
        if len(TimeStamps) >= 3:
            newTimeStampsAcc = TimeStamps[2:]
            xandy3.set_data(newTimeStampsAcc, angAccel)
            ax3.relim()
            ax3.autoscale_view()

    return xandy3

def animate_time(frame):
    global TimeStamps, dt
    
    dt = []
    for i in range(len(TimeStamps)-1):
        diffT = TimeStamps[i+1] - TimeStamps[i]
        dt.append(diffT)
    
    with lock:
        if len(TimeStamps) >= 2:
            newTimeStamps = TimeStamps[1:]
            new_dt = dt
            xandy4.set_data(newTimeStamps, new_dt)
            ax4.relim()
            ax4.autoscale_view()
            ax4.set_ylim(0, 0.3)

    return xandy4

ani1 = FuncAnimation(fig1, animate_power, frames=None, interval=100, save_count=10)
ani2 = FuncAnimation(fig2, animate_velocity, frames=None, interval=100, save_count=10)
ani3 = FuncAnimation(fig3, animate_acceleration, frames=None, interval=100, save_count=10)
ani4 = FuncAnimation(fig4, animate_time, frames=None, interval=100, save_count=10)

# Function to handle button click event
def save_data(event):
    global TimeStamps, appliedPower, angVel, angAccel, dt
    with open('plot_data.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Timestamp', 'Applied Power', 'Angular Velocity', 'Angular Acceleration', 'Dt'])
        for i in range(len(TimeStamps)):
            writer.writerow([TimeStamps[i]])
    print("Data saved to 'plot_data.csv'")

# Create a button widget
button_ax = plt.axes([0.81, 0.05, 0.1, 0.05]) # [left, bottom, width, height]
button = Button(button_ax, 'Save Data')
button.on_clicked(save_data)

plt.show()