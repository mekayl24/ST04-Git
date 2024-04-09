

##Importing neccesary libraries

import threading
import math
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from mathFunctionsPi import process_file, timeToDw, getDw, getInertia, getK, getDragPower, getAppliedPower, getsmoothedDt
import time
import RPi.GPIO as GPIO
from moving_averagePi import moving_average
from scipy.signal import savgol_filter
import tkinter as tk
from tkinter import messagebox
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg






# Initialize GPIO pin
gpio_pin = 23
GPIO.setmode(GPIO.BCM)
GPIO.setup(gpio_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Initializing Global variables
TimeStamps = []
sensor_change = [1]
initial_time = time.time()

dtTest = []


newTimeStampsPwr = [0]
newTimeStampsVel = [0]
appliedPower = [0]
#angVel = [0,0]
#angVelraw = [0]



max_power = 0
max_velocity = 0
avg_power = 0
avg_velocity = 0

interval_start_time = initial_time 

plot1 = []

plot2 = []




# Lock for thread safety
lock = threading.Lock()



def get_sensor_data():      # returns GPIO data from Raspberry Pi
    return GPIO.input(gpio_pin)


def update_data(): #Main function to record the timestamps from hall effect sensor
    global TimeStamps, sensor_change, initial_time, appliedPower, interval_start_time, dt, dtTest
    
    while True:             
        gpio_data = get_sensor_data()
        with lock:
            if gpio_data == 0 and sensor_change[-1] != 0:       #Checks if magnet is sensed by sensor and if it changed from 0 to 1
                timestamp = time.time() - initial_time
                TimeStamps.append(timestamp) #adding timestamp to list
                #print("TimeStamps: ", TimeStamps[-1])
            
                
                sensor_change.append(0) #This list adds a 0 to tell the program that we accounted for this magnet
            elif gpio_data == 1:
                sensor_change.append(1) #adds a 1 if no magnet is sensed so we can run the 
        
        current_time = time.time()  #
        # if current_time - interval_start_time >= 5 & len(appliedPower)> 1:
        #     with lock:
        #         # Update max_power to the maximum power recorded in the previous 5-second interval
        #         max_power = max(appliedPower)
        #         # Update the start time of the current 5-second interval
        #         interval_start_time = current_time
        
        time.sleep(0.01)  # Adjust sleep time as needed

# Thread for updating data
update_thread = threading.Thread(target=update_data)
update_thread.daemon = True  # Daemonize the thread so it exits when the main program ends
update_thread.start()





class StartWindow:  #GUI start window using Tkinter
    def __init__(self, root):
        self.root = root
        self.root.title("Start Window")
        self.root.attributes('-fullscreen', True)

        self.background_image = tk.PhotoImage(file="dark water 2.png") #The image for the backgorund in start menu
        self.background_label = tk.Label(root, image=self.background_image)
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)
        
        self.title_label = tk.Label(root, text="Sprint Kayak Ergometer Capstone ST04", font=("Arial Black", 30, "bold"), height = 1, bg="#3e4d87", fg="white", relief="raised", borderwidth=5)
        self.title_label.pack(pady=(250, 50)) #adjust padding

        self.enter_button = tk.Button(root, text="Enter", bg="black", fg="white",font=("Arial Black", 20,"bold"), relief="raised", borderwidth=3, cursor="hand2", command=self.switch_to_graph)
        self.enter_button.pack()

    def switch_to_graph(self):  #switching screens
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
        
        
        #variables initializing
        self.max_power = 0
        
        # Create a frame for the buttons
        self.button_frame = tk.Frame(self.root, bg="white")
        self.button_frame.pack(side=tk.TOP, fill=tk.X)

        self.start_button = tk.Button(self.button_frame, text="Start", bg="#3e4d87", fg="white",font=("Arial Black", 12,"bold"), relief="raised", borderwidth=3, cursor="hand2", command=self.start_timer)
        self.start_button.pack(side=tk.LEFT, padx=10, pady=20)

        self.stop_button = tk.Button(self.button_frame, text="Stop", bg="#3e4d87", fg="white",font=("Arial Black", 12,"bold"), relief="raised", borderwidth=3, cursor="hand2", command=self.stop_timer)
        self.stop_button.pack(side=tk.LEFT, padx=10, pady=20)

        self.exit_button = tk.Button(self.button_frame, text="Exit", bg="#3e4d87", fg="white",font=("Arial Black", 12,"bold"), relief="raised", borderwidth=3, cursor="hand2", command=self.exit)
        self.exit_button.pack(side=tk.RIGHT, padx=10, pady=20)
        
        ###display avg velocity & velocity
        self.max_velocity = tk.Label(self.button_frame, text="", font=("Arial", 12), bg="white", fg="#3e4d87", height=1)
        self.max_velocity.pack(side=tk.LEFT, padx=10, pady=10) #adjust padding
       
        self.avg_velocity = tk.Label(self.button_frame, text="", font=("Arial", 12), bg="white", fg="#3e4d87", height=1)
        self.avg_velocity.pack(side=tk.LEFT, padx=10, pady=10) #adjust padding
       
        ##display avg velocity & max power
       
        self.avg_power = tk.Label(self.button_frame, text="", font=("Arial", 12), bg="white", fg="#3e4d87", height=1)
        self.avg_power.pack(side=tk.RIGHT, padx=10, pady=10) #adjust padding
       
        self.max_power = tk.Label(self.button_frame, text="", font=("Arial", 12), bg="white", fg="#3e4d87", height=1)
        self.max_power.pack(side=tk.RIGHT, padx=10, pady=10) #adjust padding

        self.fig, (self.ax1, self.ax2) = plt.subplots(1, 2, figsize=(10,2)) #adjust the size of the graphs
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.elapsed_time_label = tk.Label(self.root, text="", font=("Arial", 20, "bold"), bg="white", fg="#3e4d87")
        self.elapsed_time_label.pack(side = tk.BOTTOM, fill=tk.X)

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
        global TimeStamps, appliedPower, plot1, plot2, angVel, newTimeStampsPwr, newTimeStampsVel, appliedPower,angVelraw, max_power, max_velocity, avg_power, avg_velocity
        current_time = time.time() - self.start_time
        self.elapsed_time_label.config(text=f"Elapsed Time: {current_time:.2f} seconds")
        ##velocity and power computations and displays
        self.max_velocity.config(text=f"Max Velocity: {max_velocity:.2f} m/s")
        self.avg_velocity.config(text=f"Avg Velocity: {avg_velocity:.2f} m/s")
        self.max_power.config(text=f"Max Power: {max_power:.2f} W")
        self.avg_power.config(text=f"Avg Power: {avg_power:.2f} W")
        #self.ax1.set_xlim(0, 10) 
        with lock:
            dt = getsmoothedDt(TimeStamps)
            freq, angVelraw, RPMvalues = timeToDw(TimeStamps, dt)
            
            
            if len(angVelraw) >= 5:
                    
                    angVel = angVelraw #uncomment for no velocity filter 
                    #angVel= savgol_filter(angVelraw, window_length=5, polyorder=3)    #uncomment for savgol filter
            else:
                    # If there are not enough data points, use the original data without smoothing
                angVel = angVelraw
            
            
            dw, angAccel = getDw(dt, angVel)
            inertia = getInertia(1.5, 0.3302)
            k = getK(angVel, angAccel, inertia)
            
            dragPow, dragTor = getDragPower(angVel, k)
            appliedPower, appliedTorque = getAppliedPower(dragTor, inertia, angAccel, angVel)
            
            if len(TimeStamps) < 2:
                
                newTimeStampsPwr = [0]
                newTimeStampsVel = [0]
                appliedPower = [0]
                angVel = [0]
                angVelraw = [0]
                                
                
            if len(TimeStamps) >= 3:
                newTimeStampsPwr = TimeStamps[2:]

                plot1 = [newTimeStampsPwr, appliedPower]
                self.ax1.relim()
                self.ax1.autoscale_view()
         
            if len(TimeStamps) >= 2:
                newTimeStampsVel = TimeStamps[1:]
            # Plot angular velocity
                plot2 = [newTimeStampsVel, angVel]
         
            
            x = newTimeStampsPwr
            y = appliedPower
            x2 = newTimeStampsVel
            y2 = angVel
            
            max_power = max(appliedPower)
            
            max_velocity = max(angVel)
            
            avg_power = sum(appliedPower) / len(appliedPower)
            
            avg_velocity = sum(angVel) / len(angVel)
            
            
            

        self.ax1.clear()
        self.ax1.plot(x, y)
        self.ax1.set_title("Applied Power in a Stroke")
        
        
        self.ax2.clear()
        self.ax2.plot(x2, y2)
        self.ax2.set_title("Angular Velocity")
        
        self.ax1.set_xlabel('Time (seconds)')  # Add x-axis title for the first subplot
        self.ax1.set_ylabel('Applied Power (W)')  # Add y-axis title for the first subplot

        self.ax2.set_xlabel('Time (seconds)')  # Add x-axis title for the second subplot
        self.ax2.set_ylabel('Angular Velocity (rad/s)')  # Add y-axis title for the second subplot


        if len(TimeStamps) > 2:
            
            interval_start_time = max(TimeStamps[-1] - 5, 0)

    # Update the x-axis limits of the first subplot
            self.ax1.set_xlim(interval_start_time, TimeStamps[-1])

    # Update the x-axis limits of the second subplot
            #self.ax2.set_xlim(interval_start_time, TimeStamps[-1])

        self.canvas.draw()

        if self.running:
            self.root.after(1, self.update_graph)  # Update every second

    def exit(self):
        if messagebox.askyesno("Exit", "Are you sure you want to exit?"):
            self.root.destroy()

def main():
    root = tk.Tk()
    app = StartWindow(root)
    root.mainloop()

if __name__ == "__main__":
    main()




