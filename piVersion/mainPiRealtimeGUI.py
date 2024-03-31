import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.animation import FuncAnimation
import numpy as np
from mathFunctionsPi import process_file, timeToDw, getDw, getInertia, getK, getDragPower, getAppliedPower, getsmoothedDt
import time
import threading
import math
import RPi.GPIO as GPIO
from moving_averagePi import moving_average
from scipy.signal import savgol_filter

##



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

##Realtime Function Defintions
"""

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

# Thread for updating data
update_thread = threading.Thread(target=update_data)
update_thread.daemon = True  # Daemonize the thread so it exits when the main program ends
update_thread.start()

"""
#un comment to do first plot
"""
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

"""

## GUI

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

        self.fig, (self.ax1, self.ax2) = plt.subplots(1, 2, figsize=(10,2)) #adjust the size of the graphs
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.elapsed_time_label = tk.Label(self.root, text="")
        self.elapsed_time_label.pack()

        self.running = False
        self.start_time = None

        # Initialize variables for animations
        self.line1, = self.ax1.plot([], [], lw=2)
        self.line2, = self.ax2.plot([], [], lw=2)

        # Initialize update thread
        self.update_thread = threading.Thread(target=self.update_data)
        self.update_thread.daemon = True
        self.update_thread.start()

    def start_timer(self):
        if not self.running:
            self.running = True
            self.start_time = time.time()
            #self.ani1 = FuncAnimation(self.fig, self.animate_power, frames=None, interval=100, blit=True)
            self.ani1 = FuncAnimation(self.fig, self.animate_power, frames=None, interval=100, save_count=10)
            self.ani2 = FuncAnimation(self.fig, self.animate_velocity, frames=None, interval=100, save_count=10)

    def stop_timer(self):
        if self.running:
            self.running = False
            self.ani1.event_source.stop()
            self.ani2.event_source.stop()

    def get_sensor_data(self):
        return GPIO.input(gpio_pin)

    def update_data(self):
        global TimeStamps, sensor_change, initial_time, appliedPower, interval_start_time, dt, dtTest
    
        while True:
            gpio_data = self.get_sensor_data()
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
            
            
            
            
            
            
            
            time.sleep(0.01)

    def update_graph(self):
        current_time = time.time() - self.start_time
        self.elapsed_time_label.config(text=f"Elapsed Time: {current_time:.2f} seconds")

        x = np.linspace(0, 10, 100)
        y = np.sin(x + time.time() - self.start_time)
        y_derivative = np.gradient(y, x)

        self.ax1.clear()
        self.ax1.plot(x, y)
        self.ax1.set_title("Sine Wave")
        
        self.ax2.clear()
        self.ax2.plot(x, y_derivative)
        self.ax2.set_title("Sine Wave Derivative")

        self.canvas.draw()

        if self.running:
            self.root.after(1, self.update_graph)  # Update every second
    
    
    def animate_power(self, frame):
        global TimeStamps, appliedPower
        print("Animating...")
        
        
        with lock:
            dt = getsmoothedDt(TimeStamps)
            freq, angVelraw, RPMvalues = timeToDw(TimeStamps, dt)
            
            if len(angVelraw) >= 5:
                angVel = savgol_filter(angVelraw, window_length=5, polyorder=3)
            else:
                angVel = angVelraw
            
            dw, angAccel = getDw(dt, angVel)
            inertia = getInertia(1.5, 0.3302)
            k = getK(angVel, angAccel, inertia)
            dragPow, dragTor = getDragPower(angVel, k)
            appliedPower, appliedTorque = getAppliedPower(dragTor, inertia, angAccel, angVel)
            
            if len(TimeStamps) >= 3:
                newTimeStampsPwr = TimeStamps[2:]
                # Plot applied power
                self.line1.set_data(newTimeStampsPwr, appliedPower)
                self.ax1.relim()  
                self.ax1.autoscale_view()  
                self.ax1.set_xlim(newTimeStampsPwr[0], newTimeStampsPwr[-1])  
                self.fig.canvas.draw_idle()  # Update the plot

        return self.line1,

    def animate_velocity(self, frame):
        global TimeStamps

        with lock:
            dtraw = [TimeStamps[i+1] - TimeStamps[i] for i in range(len(TimeStamps)-1)]
            dt = dtraw
            print("Animating...")
            freq, angVel, RPMvalues = timeToDw(TimeStamps, dt)
            
            if len(TimeStamps) >= 2:
                newTimeStampsVel = TimeStamps[1:]
                # Plot angular velocity
                self.line2.set_data(newTimeStampsVel, angVel)
                self.ax2.relim()  
                self.ax2.autoscale_view()  
                self.ax2.set_xlim(newTimeStampsVel[0], newTimeStampsVel[-1])
                self.fig.canvas.draw_idle()  # Update the plot

        return self.line2,

    def exit(self):
        if messagebox.askyesno("Exit", "Are you sure you want to exit?"):
            self.root.destroy()

def main():
    root = tk.Tk()
    app = StartWindow(root)
    root.mainloop()

if __name__ == "__main__":
    main()