import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import time

class StartWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Start Window")
        self.root.attributes('-fullscreen', True)

        self.background_image = tk.PhotoImage(file="dark water.png")
        self.background_label = tk.Label(root, image=self.background_image)
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)
       
        self.title_label = tk.Label(root, text="Welcome to My App", font=("Helvetica", 24))
        self.title_label.pack(pady=50)

        self.enter_button = tk.Button(root, text="Enter", command=self.switch_to_graph)
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

        self.background_image = tk.PhotoImage(file="dark water.png")
        self.background_label = tk.Label(self.root, image=self.background_image)
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)

        self.start_button = tk.Button(self.root, text="Start", command=self.start_timer)
        self.start_button.pack()

        self.stop_button = tk.Button(self.root, text="Stop", command=self.stop_timer)
        self.stop_button.pack()

        self.exit_button = tk.Button(self.root, text="Exit", command=self.exit)
        self.exit_button.pack()

        self.fig, (self.ax1, self.ax2) = plt.subplots(1, 2)
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