import matplotlib.pyplot as plt
import numpy as np

# outputs n amount of points where the slope of data is minimum
def minima(data, n):
    arguments = np.zeros(n)
    slope = np.diff(data)
    for i in range(0,n):
        arguments[i] = np.argmin(slope)
        slope[arguments[i]] = 0
    return arguments

# opens data file and plots data with minimum slopes
data = np.loadtxt('text')
plt.plot(data, 'b')
data_minima = minima(data,2)
for i in data_minima:
    plt.axvline(x=i, ymin=0,ymax=max(data),color='r')

data2 = np.loadtxt('text2')
plt.plot(data2,'g')
data_minima2 = minima(data2,2)
for i in data_minima2:
    plt.axvline(x=i, ymin=0,ymax=max(data),color='r')

