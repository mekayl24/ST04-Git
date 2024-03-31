#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import tkinter as tk
from tkinter import messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from matplotlib.animation import FuncAnimation
import RPi.GPIO as GPIO
import numpy as np
import time

class GraphWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Graph Window")
        self.root.attributes('-fullscreen', True)

        # Set up GPIO
        self.gpio_pin = 23
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.gpio_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

        # Initialize variables
        self.TimeStamps = []
        self.sensor_change = [1]
        self.initial_time = time.time()

        # Create a frame for the buttons
        self.button_frame = tk.Frame(self.root)
        self.button_frame.pack(side=tk.TOP, fill=tk.X)

        self.start_button = tk.Button(self.button_frame, text="Start", bg="#3e4d87", fg="white",font=("Arial Black", 12,"bold"), relief="raised", borderwidth=3, cursor="hand2", command=self.start_timer)
        self.start_button.pack(side=tk.LEFT, padx=20, pady=20)

        self.stop_button = tk.Button(self.button_frame, text="Stop", bg="#3e4d87", fg="white",font=("Arial Black", 12,"bold"), relief="raised", borderwidth=3, cursor="hand2", command=self.stop_timer)
        self.stop_button.pack(side=tk.LEFT, padx=20, pady=20)

        self.exit_button = tk.Button(self.button_frame, text="Exit", bg="#3e4d87", fg="white",font=("Arial Black", 12,"bold"), relief="raised", borderwidth=3, cursor="hand2", command=self.exit)
        self.exit_button.pack(side=tk.RIGHT, padx=20, pady=20)

        # Matplotlib figure
        self.fig = Figure(figsize=(8, 6), dpi=100)
        self.ax = self.fig.add_subplot(111)
        self.ax.set_xlabel('Timestamp')
        self.ax.set_ylabel('Applied Power')

        # Embed Matplotlib figure into Tkinter window
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.pack(fill=tk.BOTH, expand=True)

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

    def update_data(self):
        gpio_data = GPIO.input(self.gpio_pin)
        
        if gpio_data == 0 and self.sensor_change[-1] != 0:
            timestamp = time.time() - self.initial_time
            
            self.TimeStamps.append(timestamp)
            self.sensor_change.append(0)
        if gpio_data == 1:
            self.sensor_change.append(1)

    def animate(self, frame):
        self.update_data()
        
        # Your code for calculating applied power and updating the graph goes here
        # Make sure to update the graph using self.ax.plot(x, y) and self.canvas.draw()

        return xandy

    def exit(self):
        if messagebox.askyesno("Exit", "Are you sure you want to exit?"):
            self.root.destroy()

def main():
    app = GraphWindow()
    app.root.mainloop()

if __name__ == "__main__":
    main()

