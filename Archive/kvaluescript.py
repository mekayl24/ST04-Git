
import math
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from mathFunctionsPi import process_file, timeToDw, getDw, getInertia, getK, getDragPower, getAppliedPower, getsmoothedDt
from moving_averagePi import moving_average
from scipy.signal import savgol_filter

TimeStamps = process_file("/home/pi/ST04-Git/Trials/Kvalues.txt")


###Moving Average Filter

dt = getsmoothedDt(TimeStamps)


