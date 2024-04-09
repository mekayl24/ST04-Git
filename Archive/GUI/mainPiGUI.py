import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.animation import FuncAnimation
import numpy as np
import time
import threading

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
            self.ani1 = FuncAnimation(self.fig, self.animate_power, frames=None, interval=100, blit=True)
            self.ani2 = FuncAnimation(self.fig, self.animate_velocity, frames=None, interval=100, blit=True)

    def stop_timer(self):
        if self.running:
            self.running = False
            self.ani1.event_source.stop()
            self.ani2.event_source.stop()

    def update_data(self):
        global TimeStamps
        while True:
            # Update your data here
            time.sleep(0.01)

    def animate_power(self, frame):
        # Update your applied power data here
        x = np.linspace(0, 10, 100)
        y = np.sin(x + time.time() - self.start_time)
        self.line1.set_data(x, y)
        self.ax1.set_title("Sine Wave")
        return self.line1,

    def animate_velocity(self, frame):
        # Update your angular velocity data here
        x = np.linspace(0, 10, 100)
        y = np.cos(x + time.time() - self.start_time)
        self.line2.set_data(x, y)
        self.ax2.set_title("Cosine Wave")
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