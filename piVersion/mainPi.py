
import math
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from mathFunctionsPi import process_file, timeToDw, getDw, getInertia, getK, getDragPower, getAppliedPower, getsmoothedDt
from moving_averagePi import moving_average
#from scipy.signal import savgol_filter







TimeStamps = process_file("C:\\Users\\mekay\\Documents\\GitHub\\ST04\\spin up then spin down.txt")


###Moving Average Filter

#dt = getsmoothedDt(TimeStamps)



###No Filter

dtraw = []
for i in range(len(TimeStamps)-1):
    newStamp = TimeStamps[i+1] - TimeStamps[i] #Calculating all values
    dtraw.append(newStamp)  

dt = dtraw



###SavGol Filter
"""
dtraw = dt
for i in range(len(TimeStamps)-1):
    newStamp = TimeStamps[i+1] - TimeStamps[i] #Calculating all values
    dtraw.append(newStamp)  


#dt = savgol_filter(dtraw, window_length=5, polyorder=3)

dt = dtraw
"""

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





plt.figure()
plt.plot(TimeStamps[timeInitIndex:timeFinIndex], appliedPower[pwrInitIndex:pwrFinIndex], marker='o', linestyle='-',
         color='b', label='Data Points') #Plotting whole curve


# Add labels and title
plt.xlabel('Time (seconds)')
plt.ylabel('Power (Watts)')
plt.title('Power within a single stroke')


plt.xlim(0, 14)  # Adjust x-axis limits to zoom in on a specific section
#plt.ylim(0, 50)  # Adjust y-axis limits if needed
# Add gridlines
plt.grid(True)

# Show legend
plt.legend()

# Adjust plot layout
plt.tight_layout()




#####Ang Vel over session
"""

plt.figure()
plt.plot(TimeStamps[timeInitIndex:timeFinIndex], angVel[pwrInitIndex-1:pwrFinIndex-1], marker='o', linestyle='-',
         color='b', label='Data Points') #Plotting whole curve


# Add labels and title
plt.xlabel('Time (seconds)')
plt.ylabel('PRPM')
plt.title('RPM within a all strokes')

# Add gridlines
plt.grid(True)

# Show legend
plt.legend()

# Adjust plot layout
plt.tight_layout()

# Show the plot


"""



plt.figure()
plt.plot(TimeStamps[timeInitIndex:timeFinIndex], RPMvalues[pwrInitIndex-1:pwrFinIndex-1], marker='o', linestyle='-',
         color='b', label='Data Points') #Plotting whole curve


# Add labels and title
plt.xlabel('Time (seconds)')
plt.ylabel('Ang Velocity (RPM)')
plt.title('Ang Velocity within a session (No filter, 16 Magnets))')

plt.xlim(0, 14)  # Adjust x-axis limits to zoom in on a specific section
plt.ylim(0, 650)  # Adjust y-axis limits if needed

# Add gridlines
plt.grid(True)

# Show legend
plt.legend()

# Adjust plot layout
plt.tight_layout()


# Show the plot


# Ang acceleration plo


plt.figure()
plt.plot(TimeStamps[timeInitIndex:timeFinIndex], angAccel[pwrInitIndex:pwrFinIndex], marker='o', linestyle='-',
         color='b', label='Data Points') #Plotting whole curve


# Add labels and title
plt.xlabel('Time (seconds)')
plt.ylabel('Angular Accleration)')
plt.title('Acceleration throughout session')


#plt.xlim(0, 14)  # Adjust x-axis limits to zoom in on a specific section
#plt.ylim(0, 50)  # Adjust y-axis limits if needed
# Add gridlines
plt.grid(True)

# Show legend
plt.legend()

# Adjust plot layout
plt.tight_layout()

plt.show()