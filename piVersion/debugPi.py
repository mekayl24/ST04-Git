import math
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from mathFunctions import process_file, timeToDw, getDw, getInertia, getK, getDragPower, getAppliedPower, moving_average

TimeStamps = process_file("C:\\Users\\mekay\\Desktop\\Capstone\\Code 27Feb\\Trial 9 Data.txt")
dt, freq, angVel, RPMvalues = timeToDw(TimeStamps)
dw, angAccel = getDw(dt,angVel)
inertia =(getInertia(1.5, 0.3302))
k = getK(angVel,angAccel,inertia)
dragPow, dragTor = getDragPower(angVel, k)
appliedPower, appliedTorque = getAppliedPower(dragTor, inertia, angAccel, angVel)

#print(appliedPower)



smoothed_dt = moving_average(dt, 4)


timeInitIndex = 3
timeFinIndex = len(TimeStamps)
pwrInitIndex = 1
pwrFinIndex = len(appliedPower)

plt.figure()

## Zoomed in graph
plt.plot(TimeStamps[timeInitIndex:timeFinIndex], smoothed_dt[2:404], marker='o', linestyle='-', color='b', label='Zoomed In')
plt.xlabel('Time (seconds)')
plt.ylabel('Dt')
plt.title('Dt vs Time stamps')
plt.xlim(0, 10)  # Adjust x-axis limits to zoom in on a specific section
plt.ylim(0, 0.5)  # Adjust y-axis limits if needed
plt.grid(True)
plt.legend()
plt.tight_layout()


plt.show()