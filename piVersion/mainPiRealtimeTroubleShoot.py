import threading
import math
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from mathFunctionsPi import process_file, timeToDw, getDw, getInertia, getK, getDragPower, getAppliedPower, getsmoothedDt
import time
import RPi.GPIO as GPIO
from moving_averagePi import moving_average
import csv
import os
import atexit

# Initialize GPIO pin
gpio_pin = 23
GPIO.setmode(GPIO.BCM)
GPIO.setup(gpio_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Global variables
TimeStamps = []
sensor_change = [1]
initial_time = time.time()
appliedPower = [1]

# max_power = 0.0

interval_start_time = initial_time 
# Lock for thread safety
lock = threading.Lock()

def get_sensor_data():
    return GPIO.input(gpio_pin)

def update_data(dt):
    global TimeStamps, sensor_change, initial_time, appliedPower, interval_start_time
    
    while True:
        try:
            gpio_data = get_sensor_data()
            with lock:
                if gpio_data == 0 and sensor_change[-1] != 0:
                    timestamp = time.time() - initial_time
                    TimeStamps.append(timestamp)
                    # print(TimeStamps[-1])
                    # print("Dt: ", dt)
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
        except KeyboardInterrupt:
            pass

# Register a function to be called on script exit
def save_csv_on_exit():
    print("Saving data to CSV...")
    save_csv()
    print("Data saved successfully.")

# Thread for updating data
update_thread = threading.Thread(target=update_data, args=(None,))
update_thread.daemon = True  # Daemonize the thread so it exits when the main program ends
update_thread.start()

# Plot initialization for applied power
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

# Plot initialization for angular acceleration
fig3, ax3 = plt.subplots()
xandy3, = ax3.plot([], [], lw=2)
ax3.set_title('Real-time Angular Acceleration Plot')
ax3.set_xlabel('Timestamp')
ax3.set_ylabel('Angular Acceleration')

# Plot initialization for timestamps
fig4, ax4 = plt.subplots()
xandy4, = ax4.plot([], [], lw=2)
ax4.set_title('Real-time Dt')
ax4.set_xlabel('Timestamp')
ax4.set_ylabel('Dt')

plt.show(block=False)

# Data to be saved
data_to_save = {
    "TimeStamps": TimeStamps,
    "dt": [],
    "angVel": [],
    "RPMvalues": [],
    "angAccel": [],
    "appliedPower": [],
    "dragPow": [],
    "dragTor": []
}

# Save CSV function
def save_csv():
    folder_path = "/home/pi/ST04-GIt"
    file_name = "data.csv"
    file_path = os.path.join(folder_path, file_name)
    
    with open(file_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(data_to_save.keys())
        writer.writerows(zip(*data_to_save.values()))
    print("Data saved successfully.")

# Register the function to be called on script exit
atexit.register(save_csv_on_exit)

# Animation function for applied power
def animate_power(frame):
    global TimeStamps, appliedPower, data_to_save
    
    with lock:
        dt = getsmoothedDt(TimeStamps)
        data_to_save["dt"] = dt
        
        freq, angVel, RPMvalues = timeToDw(TimeStamps, dt)
        data_to_save["angVel"] = angVel
        data_to_save["RPMvalues"] = RPMvalues
        
        dw, angAccel = getDw(dt, angVel)
        data_to_save["angAccel"] = angAccel
        
        inertia = getInertia(1.5, 0.3302)
        k = getK(angVel, angAccel, inertia)
        dragPow, dragTor = getDragPower(angVel, k)
        data_to_save["dragPow"] = dragPow
        data_to_save["dragTor"] = dragTor
        
        appliedPower, appliedTorque = getAppliedPower(dragTor, inertia, angAccel, angVel)
        data_to_save["appliedPower"] = appliedPower
        
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
    global TimeStamps
    
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
    global TimeStamps
    
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

# Animation function for timestamps
def animate_time(frame):
    global TimeStamps
    
    dt = []
    for i in range(len(TimeStamps)-1):
        diffT = TimeStamps[i+1] - TimeStamps[i]
        dt.append(diffT)
    
    with lock:
        if len(TimeStamps) >= 2:
            newTimeStamps = TimeStamps[1:]
            new_dt = moving_average(dt, 100)  # Use only available dt data
            
            # Plot timestamps
            xandy4.set_data(newTimeStamps, new_dt)
            
            # Auto-adjust Y-axis to the maximum value of the last interval
            ax4.relim()
            ax4.autoscale(axis='y') 
            
            # Set X-axis limit to show only the last 5 seconds
            ax4.set_xlim(newTimeStamps[-1] - 5, newTimeStamps[-1])
            
            # Update data to be saved
            data_to_save["dt"] = new_dt
    
    return xandy4

# Animation for applied power
ani1 = FuncAnimation(fig1, animate_power, frames=None, interval=1000, save_count=10)

# Animation for angular velocity
ani2 = FuncAnimation(fig2, animate_velocity, frames=None, interval=1000, save_count=10)

# Animation for angular acceleration
ani3 = FuncAnimation(fig3, animate_acceleration, frames=None, interval=1000, save_count=10)

# Animation for timestamps
ani4 = FuncAnimation(fig4, animate_time, frames=None, interval=1000, save_count=10)
