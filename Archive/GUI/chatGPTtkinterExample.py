import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np

# Create a Tkinter window
root = tk.Tk()
root.title("Real-time Plotting")

# Create a Matplotlib figure
fig, ax = plt.subplots()
x_data = []
y_data = []
line, = ax.plot([], [], lw=2)

# Set up the plot parameters
ax.set_xlim(0, 10)
ax.set_ylim(-1.5, 1.5)

# Function to update the plot data for animation
def update(frame):
    x_data.append(frame)
    y_data.append(np.sin(frame))
    line.set_data(x_data, y_data)
    return line,

# Create the animation
ani = FuncAnimation(fig, update, frames=np.linspace(0, 10, 100), interval=100)

# Embed the Matplotlib animation in the Tkinter window
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.draw()
canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

# Create a frame for buttons
button_frame = ttk.Frame(root)
button_frame.pack(side=tk.BOTTOM)

# Function to handle button click events
def select_graph(graph_type):
    if graph_type == "Sine Wave":
        ax.set_title("Sine Wave")
    elif graph_type == "Cosine Wave":
        ax.set_title("Cosine Wave")
    canvas.draw()

# Add buttons for selecting graph types
sine_button = ttk.Button(button_frame, text="Sine Wave", command=lambda: select_graph("Sine Wave"))
sine_button.pack(side=tk.LEFT, padx=5, pady=5)

cosine_button = ttk.Button(button_frame, text="Cosine Wave", command=lambda: select_graph("Cosine Wave"))
cosine_button.pack(side=tk.LEFT, padx=5, pady=5)

# Start the Tkinter event loop
root.mainloop()