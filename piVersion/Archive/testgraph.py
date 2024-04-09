#!/usr/bin/env python
# coding: utf-8

# In[1]:


import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import time





import math
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from mathFunctionsPi import process_file, timeToDw, getDw, getInertia, getK, getDragPower, getAppliedPower, getsmoothedDt
from moving_averagePi import moving_average
#from scipy.signal import savgol_filter







TimeStamps = process_file("C:\\Users\\mekay\\Documents\\GitHub\\ST04\\ktest.txt")


###Moving Average Filter

dt = getsmoothedDt(TimeStamps)



###No Filter
"""
dtraw = []
for i in range(len(TimeStamps)-1):
    newStamp = TimeStamps[i+1] - TimeStamps[i] #Calculating all values
    dtraw.append(newStamp)  

dt = dtraw

"""

###SavGol Filter

dtraw = dt
for i in range(len(TimeStamps)-1):
    newStamp = TimeStamps[i+1] - TimeStamps[i] #Calculating all values
    dtraw.append(newStamp)  


#dt = savgol_filter(dtraw, window_length=5, polyorder=3)

dt = dtraw


##########
freq, angVel, RPMvalues = timeToDw(TimeStamps, dt)


dw, angAccel = getDw(dt,angVel)
inertia =(getInertia(1.5, 0.3302))
k = getK(angVel,angAccel,inertia)
dragPow, dragTor = getDragPower(angVel, k)
appliedPower, appliedTorque = getAppliedPower(dragTor, inertia, angAccel, angVel)




#print(TimeStamps.index(36.903112)) #Finding when seconds 37 and 38 are, manually
#print(TimeStamps.index(38.072464))
print("Lenght of Timestamps: ", len(TimeStamps))
print("Lenght of power values: ", len(appliedPower))



# timestamps is offset from appliedpower because it differentiates twice 


timeInitIndex = 3
timeFinIndex = len(TimeStamps)
pwrInitIndex = 1
pwrFinIndex = len(appliedPower)

# sizetime = timeFinIndex - timeInitIndex
# sizepwr = pwrFinIndex - pwrInitIndex

# print("Actual size of time: ", sizetime)
# print("Actual size of pwr: ", sizepwr)





#### Debug code, just trying to see what values output for these indices
# print("timeindex: ", TimeStamps[0:6])
# print("powerindex: ", appliedPower[0:6])

###Power over session
"""

plt.figure()
plt.plot(TimeStamps[timeInitIndex:timeFinIndex], appliedPower[pwrInitIndex:pwrFinIndex], marker='o', linestyle='-',
         color='b', label='Data Points') #Plotting whole curve


# Add labels and title
plt.xlabel('Time (seconds)')
plt.ylabel('Power (Watts)')
plt.title('Power within a all strokes')

# Add gridlines
plt.grid(True)

# Show legend
plt.legend()

# Adjust plot layout
plt.tight_layout()


"""

####Dt graph with limits
"""

plt.figure()

## Zoomed in graph
plt.plot(TimeStamps[timeInitIndex:timeFinIndex], dt[timeInitIndex-1:timeFinIndex], marker='o', linestyle='-', color='b', label='Zoomed In')
plt.xlabel('Time (seconds)')
plt.ylabel('Dt')
plt.title('Dt vs Time stamps')
plt.xlim(0, 10)  # Adjust x-axis limits to zoom in on a specific section
plt.ylim(0, 0.2)  # Adjust y-axis limits if needed
plt.grid(True)
plt.legend()
plt.tight_layout()

"""

""
###Acceleration with Limits

"""

plt.figure()

## Zoomed in graph
plt.plot(TimeStamps[timeInitIndex:timeFinIndex], angAccel[pwrInitIndex:pwrFinIndex], marker='o', linestyle='-', color='b', label='Zoomed In')
plt.xlabel('Time (seconds)')
plt.ylabel('Ang Accel')
plt.title('Acceleration')
plt.xlim(8, 35)  # Adjust x-axis limits to zoom in on a specific section
plt.ylim(-10, 20)  # Adjust y-axis limits if needed
plt.grid(True)
plt.legend()
plt.tight_layout()


"""


####Power with Limits

x1 = TimeStamps[timeInitIndex:timeFinIndex]
y1 = appliedPower[pwrInitIndex:pwrFinIndex]

x2 = TimeStamps[timeInitIndex:timeFinIndex]
y2 = RPMvalues[pwrInitIndex-1:pwrFinIndex-1]







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

    def start_timer(self):
        if not self.running:
            self.running = True
            self.start_time = time.time()
            self.update_graph()

    def stop_timer(self):
        if self.running:
            self.running = False

    def update_graph(self):
        
    # Retrieve x1, y1, x2, y2 data here
        x1 = TimeStamps[timeInitIndex:timeFinIndex]
        y1 = appliedPower[pwrInitIndex:pwrFinIndex]
        x2 = TimeStamps[timeInitIndex:timeFinIndex]
        y2 = RPMvalues[pwrInitIndex-1:pwrFinIndex-1]

        self.ax1.clear()
        self.ax1.plot(x1, y1)
        self.ax1.set_title("Applied Power")
        self.ax1.set_xlabel("Time (seconds)")
        self.ax1.set_ylabel("Power (Watts)")
        #self.ax1.legend()
        #self.ax1.grid(True)
        self.ax1.set_xlim(17.5, 18.5)


        self.ax2.clear()
        self.ax2.plot(x2, y2)
        self.ax2.set_title("RPM Values")
        self.ax2.set_xlabel("Time (seconds)")
        self.ax2.set_ylabel("RPM")
        #self.ax2.legend()
        #self.ax2.grid(True)

        self.canvas.draw()

        if self.running:
            self.root.after(1000, self.update_graph)  # Update every second

    def exit(self):
        if messagebox.askyesno("Exit", "Are you sure you want to exit?"):
            self.root.destroy()

def main():
    root = tk.Tk()
    app = StartWindow(root)
    root.mainloop()

if __name__ == "__main__":
    main()


# In[ ]:




