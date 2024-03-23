
import math
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from mathFunctions import process_file, timeToDw, getDw, getInertia, getK, getDragPower, getAppliedPower, getsmoothedDt







TimeStamps = process_file("C:\\Users\\mekay\\Desktop\\Capstone\\Code 27Feb\\Trial 9 Data.txt")

dt = getsmoothedDt(TimeStamps)

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

# Show the plot



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





plt.figure()

## Zoomed in graph
plt.plot(TimeStamps[timeInitIndex:timeFinIndex], angAccel[pwrInitIndex:pwrFinIndex], marker='o', linestyle='-', color='b', label='Zoomed In')
plt.xlabel('Time (seconds)')
plt.ylabel('Ang Accel')
plt.title('Acceleration')
plt.xlim(0, 7.5)  # Adjust x-axis limits to zoom in on a specific section
plt.ylim(-10, 60)  # Adjust y-axis limits if needed
plt.grid(True)
plt.legend()
plt.tight_layout()






plt.figure()
plt.plot(TimeStamps[timeInitIndex:timeFinIndex], appliedPower[pwrInitIndex:pwrFinIndex], marker='o', linestyle='-',
         color='b', label='Data Points') #Plotting whole curve


# Add labels and title
plt.xlabel('Time (seconds)')
plt.ylabel('Power (Watts)')
plt.title('Power within a single stroke')


plt.xlim(0, 3)  # Adjust x-axis limits to zoom in on a specific section
plt.ylim(-5, 60)  # Adjust y-axis limits if needed
# Add gridlines
plt.grid(True)

# Show legend
plt.legend()

# Adjust plot layout
plt.tight_layout()


plt.show()
# Show the plot

# Process the numbers using the defined function
#processed_numbers = process_numbers(numbers_list)






###This is code for trying to animate with the raspberry pi, wont work on desktop


# def animate(frames):

#     TimeStamps = []


#     while True:


#         #line = (ser.readline().decode().strip())

#         gpio_data = GPIO.input(gpio_pin)
        
#         if gpio_data == 0 and sensor_change[-1] != 0:
#             timestamp = time.time() - initial_time
#             TimeStamps.append(timestamp)
#             print("Timestamp: ",timestamp)
#             sensor_change.append(0)
#             #print(sensor_change)
#         if gpio_data == 1:
#             sensor_change.append(1)
#         #time.sleep(0.1)


#         #timeValue = float(line)
#         #TimeStamps.append(timeValue)

#         dt, freq, angVel, RPMvalues = timeToDw(TimeStamps)
#         dw, angAccel = getDw(dt,angVel)
#         inertia =(getInertia(1.5, 0.3302))
#         k = getK(angVel,angAccel,inertia)
#         dragPow, dragTor = getDragPower(angVel, k)
#         appliedPower, appliedTorque = getAppliedPower(dragTor, inertia, angAccel, angVel)
#         if len(TimeStamps)>= 3:
#             newTimeStamps = TimeStamps[2:]
#             #print("Time:", newTimeStamps)
#             #print("Power: ", appliedPower)
#             xandy.set_data(newTimeStamps,appliedPower)
#             ax.relim()
#             ax.autoscale_view()
#         plt.draw()
#         #plt.pause(0.0001)
#         #return xandy
        
# def getSensorData():
#     gpio_pin = 23

#     GPIO.setmode(GPIO.BCM)
#     GPIO.setup(gpio_pin, GPIO.IN, pull_up_down= GPIO.PUD_UP)


 
        
#     gpio_data = GPIO.input(gpio_pin)

#     print("Data: ", gpio_data)
        
#     time.sleep(1)
        
        


#ser = serial.Serial('COM5', 9600)

# gpio_pin = 23

# GPIO.setmode(GPIO.BCM)
# GPIO.setup(gpio_pin, GPIO.IN, pull_up_down= GPIO.PUD_UP)

# TimeStamps = [0]
# sensor_change = [1]
# initial_time = time.time()

# x_data = []
# y_data = []
# fig, ax = plt.subplots()
# xandy, = ax.plot([], [], lw=2)

# plt.title('Real-time Applied Power Plot')
# plt.xlabel('Timestamp')
# plt.ylabel('Applied Power')

# plt.show(block=False)



# animate(frames = None)

#ani = FuncAnimation(fig, animate, frames=None ,interval = 100, save_count= 1000)

