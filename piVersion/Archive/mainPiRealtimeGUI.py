#!/usr/bin/env python
# coding: utf-8

# In[1]:

import threading
import math
import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import time
from matplotlib.animation import FuncAnimation
from mathFunctionsPi import process_file, timeToDw, getDw, getInertia, getK, getDragPower, getAppliedPower, getsmoothedDt
import RPi.GPIO as GPIO
from moving_averagePi import moving_average
from scipy.signal import savgol_filter




class StartWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Start Window")
        self.root.attributes('-fullscreen', True)

        self.background_image = tk.PhotoImage(file="dark water 2.png")
        self.background_label = tk.Label(root, image=self.background_image)
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)
        
        self.title_label = tk.Label(root, text="Sprint Kayak Ergometer Capstone ST04", font=("Arial Black", 40, "bold"), height = 1, bg="#3e4d87", fg="white", relief="raised", borderwidth=5)
        self.title_label.pack(pady=(300, 50)) #adjust padding

        self.enter_button = tk.Button(root, text="Enter", bg="black", fg="white",font=("Arial Black", 24,"bold"), relief="raised", borderwidth=3, cursor="hand2", command=self.switch_to_graph)
        self.enter_button.pack()

    def switch_to_graph(self):
        self.root.attributes('-fullscreen', False)
        self.root.destroy()
        GraphWindow()

class GraphWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Graph Window")
        self.root.attributes('-fullscreen', True)

        self.background_image = tk.PhotoImage(file="dark water 2.png")
        self.background_label = tk.Label(self.root, image=self.background_image)
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)
        
        # Create a frame for the buttons
        self.button_frame = tk.Frame(self.root)
        self.button_frame.pack(side=tk.TOP, fill=tk.X)

        self.start_button = tk.Button(self.button_frame, text="Start", bg="#3e4d87", fg="white",font=("Arial Black", 12,"bold"), relief="raised", borderwidth=3, cursor="hand2", command=self.start_timer)
        self.start_button.pack(side=tk.LEFT, padx=20, pady=20)

        self.stop_button = tk.Button(self.button_frame, text="Stop", bg="#3e4d87", fg="white",font=("Arial Black", 12,"bold"), relief="raised", borderwidth=3, cursor="hand2", command=self.stop_timer)
        self.stop_button.pack(side=tk.LEFT, padx=20, pady=20)

        self.exit_button = tk.Button(self.button_frame, text="Exit", bg="#3e4d87", fg="white",font=("Arial Black", 12,"bold"), relief="raised", borderwidth=3, cursor="hand2", command=self.exit)
        self.exit_button.pack(side=tk.RIGHT, padx=20, pady=20)
        
        ###display avg velocity & velocity
        self.max_velocity = tk.Label(self.button_frame, text="Max Session Velocity", font=("Arial", 14), bg="white", fg="#3e4d87", relief="ridge", borderwidth=1)
        self.max_velocity.pack(side=tk.LEFT, padx=20, pady=20) #adjust padding
        
        self.max_velocity = tk.Label(self.button_frame, text="Average Session Velocity", font=("Arial", 14), bg="white", fg="#3e4d87", relief="raised", borderwidth=1)
        self.max_velocity.pack(side=tk.LEFT, padx=20, pady=20) #adjust padding
        
        ##display avg velocity & max velocity

        self.fig, (self.ax1, self.ax2) = plt.subplots(1, 2, figsize=(10,2)) #adjust the size of the graphs
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.elapsed_time_label = tk.Label(self.root, text="", font=("Arial", 18, "bold"), bg="white", fg="#3e4d87",)
        self.elapsed_time_label.pack()

        self.running = False
        self.start_time = None

    def start_timer(self):
        if not self.running:
            self.running = True
            self.start_time = time.time()
            self.update_graph()

    def stop_timer(self):
        if self.running:
            self.running = False

    def update_graph(self):
        current_time = time.time() - self.start_time
        self.elapsed_time_label.config(text=f"Elapsed Time: {current_time:.2f} seconds")

#         x = np.linspace(0, 10, 100)
#         y = np.sin(x + time.time() - self.start_time)
#         y_derivative = np.gradient(y, x)

#         self.ax1.clear()
#         self.ax1.plot(x, y)
#         self.ax1.set_title("Sine Wave")
        
#         self.ax2.clear()
#         self.ax2.plot(x, y_derivative)
#         self.ax2.set_title("Sine Wave Derivative")
        
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



        self.canvas.draw()
    
        # Animation for applied power
        ani = FuncAnimation(fig1, animate_power, frames=None, interval=100, save_count=10)

        # Animation for angular velocity
        ani2 = FuncAnimation(fig2, animate_velocity, frames=None, interval=100, save_count=10)
        
        #plt.show()

        if self.running:
            self.root.after(1, self.update_graph)  # Update every second
    
    
    
    def exit(self):
        if messagebox.askyesno("Exit", "Are you sure you want to exit?"):
            self.root.destroy()


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
                    print("TimeStamps: ", TimeStamps[-1])
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
            

def animate_power(frame):
        global TimeStamps, appliedPower

        with lock:
            dt = getsmoothedDt(TimeStamps)
            freq, angVelraw, RPMvalues = timeToDw(TimeStamps, dt)


            if len(angVelraw) >= 5:
                    angVel= savgol_filter(angVelraw, window_length=5, polyorder=3)
            else:
                    # If there are not enough data points, use the original data without smoothing
                angVel = angVelraw


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
            #dt = getsmoothedDt(TimeStamps)
            dtraw = []
            for i in range(len(TimeStamps)-1):
                newStamp = TimeStamps[i+1] - TimeStamps[i] #Calculating all values
                dtraw.append(newStamp)  

            dt = dtraw

            freq, angVel, RPMvalues = timeToDw(TimeStamps, dt)

            if len(TimeStamps) >= 2:
                newTimeStampsVel = TimeStamps[1:]
                # Plot angular velocity
                xandy2.set_data(newTimeStampsVel, angVel)
                ax2.relim()
                ax2.autoscale_view()
                #ax2.set_xlim(newTimeStampsVel[-1] - 5, newTimeStampsVel[-1])

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
               # ax3.set_xlim(newTimeStampsAcc[-1] - 5, newTimeStampsAcc[-1])

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
                #ax4.set_xlim(newTimeStamps[-1] - 5, newTimeStamps[-1])

                # Set the maximum value of the y-axis to 0.3
                ax4.set_ylim(0, 0.3)

        return xandy4

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
lock = threading.Lock()

def main():
    root = tk.Tk()
    
    app = StartWindow(root)
    update_thread = threading.Thread(target=update_data)
    update_thread.daemon = True  # Daemonize the thread so it exits when the main program ends
    update_thread.start()
    root.mainloop()

if __name__ == "__main__":
    main()


# In[ ]:




