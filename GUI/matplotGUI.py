import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np

# Create a figure and axis
fig, ax = plt.subplots()
x_data = []
y_data = []

# Set up the plot parameters
ax.set_xlim(0, 10)
ax.set_ylim(-1.5, 1.5)
line, = ax.plot([], [], lw=2)

# Function to update the plot data for animation
def update(frame):
    x = np.linspace(0, 10, 100)
    y = np.sin(x + frame/10)
    line.set_data(x, y)
    return line,

# Create the animation
ani = FuncAnimation(fig, update, frames=np.arange(0, 100), interval=100)

# Show the plot
plt.show()