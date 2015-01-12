import visa
import matplotlib.pyplot as plt
import numpy as np

##parameters
center_frequency = 4607000
frequency_span = 2000
bandwidth = 300
data_points = 11
sweep_count = 2
minimum_power = -1
maximum_power = 1

#export parameters
parameters = [
center_frequency,
frequency_span,
bandwidth,
data_points,
sweep_count,
minimum_power,
maximum_power
]
np.save('test_parameters',parameters)

##initialization
#connect to NA
rm = visa.ResourceManager()
#print(rm.list_resources())
inst = rm.open_resource('GPIB0::17::INSTR')
#print(inst.query('*IDN?'))

#NA initialization
inst.write('CENT '+str(center_frequency))  #\set the frequency range of the sweep
inst.write('SPAN '+str(frequency_span))    #/
inst.write('BWAUTO OFF')                #\set the IF bandwidth
inst.write('BW '+str(bandwidth))        #/
inst.write('FMT LINM')  #set NA screen format
inst.write('POIN '+str(data_points))  #set number of points
inst.write('CIRF LIN') #set data format
inst.write('*SRE 4;ESNB 1') #sets interrupt on sweep end
frequency_range = np.linspace(center_frequency-frequency_span/2,center_frequency+frequency_span/2,data_points)
    
#data initialization
amplitudes_forward_real = np.zeros([sweep_count,data_points])
amplitudes_forward_imaginary = np.zeros([sweep_count,data_points])
magnitudes_forward = np.zeros([sweep_count,data_points])

points_backward = np.zeros([data_points,4]) #the NA analyzes 2 points (start and end), and they contain real and imaginary values, so that makes 4 points
amplitudes_backward_real = np.zeros([sweep_count,data_points])
amplitudes_backward_imaginary = np.zeros([sweep_count,data_points])
magnitudes_backward = np.zeros([sweep_count,data_points])

power = np.linspace(minimum_power,maximum_power,sweep_count)

plt.figure
plt.xlim(center_frequency-frequency_span/2,center_frequency+frequency_span/2,data_points)

##sweep
for i in range(sweep_count):
    inst.write('POWE '+str(power[i]))
    
    #measurement
    inst.write('CLES') # clear all status registers
    inst.write('SING')
    inst.wait_for_srq()
    
    #print to NA screen
    inst.write('AUTO') #automatically scales data
    
    #save data
    amplitudes_forward = inst.query_ascii_values('OUTPDATA?')
    amplitudes_forward_real[i] = np.array(amplitudes_forward[::2])
    amplitudes_forward_imaginary[i] = np.array(amplitudes_forward[1::2])
    magnitudes_forward[i] = np.sqrt(np.multiply(amplitudes_forward_real[i], amplitudes_forward_real[i]) + np.multiply(amplitudes_forward_imaginary[i], amplitudes_forward_imaginary[i])) #quadratic sum of imaginary and real terms  
    #print to computer screen
    plt.plot(frequency_range,magnitudes_forward[i])
    #backwards sweep: the NA has no built-in backwards sweep. Therefore a 2-points, SPAN 0 sweep is repeated for # of data points to simulate the backwards sweep. 
    inst.write('SPAN 0')
    inst.write('POIN 2')
    for j in range(data_points):
        inst.write('CENT '+str(frequency_range[-1-j]))#set frequency (frequency range is reversed for backwards sweep)
        inst.write('CLES') # clear all status registers
        inst.write('SING')
        inst.wait_for_srq()
        points_backward[j] = inst.query_ascii_values('OUTPDATA?')
    for k in range(data_points):
        amplitudes_backward_real[i] = (points_backward[:,0]+ points_backward[:,2])/2
        amplitudes_backward_imaginary[i] = (points_backward[:,1]+ points_backward[:,3])/2
        magnitudes_backward[i] = np.sqrt(np.multiply(amplitudes_backward_real[i], amplitudes_backward_real[i]) + np.multiply(amplitudes_backward_imaginary[i], amplitudes_backward_imaginary[i]))
    plt.plot(frequency_range[::-1],magnitudes_backward[i])
    inst.write('CENT '+str(center_frequency))  #\reset the frequency range of the sweep
    inst.write('SPAN '+str(frequency_span))    #/
    inst.write('POIN '+str(data_points))  #reset number of points
    
inst.write('CLES') # clear all status registers  
np.save('test_forward_real', amplitudes_forward_real)
np.save('test_forward_imaginary',amplitudes_forward_imaginary)
np.save('test_forward_magnitudes',magnitudes_forward)
np.save('test_backward_real', amplitudes_backward_real)
np.save('test_backward_imaginary',amplitudes_backward_imaginary)
np.save('test_backward_magnitudes',magnitudes_backward)

##transistion points
def minima(data, n):
    arguments = np.zeros(n) #initialize arguments
    slope = np.diff(data)   #differentiaties data
    for i in range(0,n):
        arguments[i] = np.argmin(slope)
        slope[arguments[i]] = 0
    return arguments

def maxima(data, n):
    arguments = np.zeros(n) #initialize arguments
    slope = np.diff(data)   #differentiaties data
    for i in range(0,n):
        arguments[i] = np.argmax(slope)
        slope[arguments[i]] = 0
    return arguments

#determine the downward and upward transistion points. First the arguments of the transitions in the array are found. Afterwards the corresponding frequencies are calculated.
forward_magnitudes = np.load('test_forward_magnitudes.npy')
backward_magnitudes = np.load('test_backward_magnitudes.npy')

downward_transition_points = np.zeros(sweep_count)
upward_transition_points = np.zeros(sweep_count)
downward_transition_frequencies = np.zeros(sweep_count) 
upward_transition_frequencies = np.zeros(sweep_count)

for i in range(sweep_count):
    downward_transition_points[i] = minima(forward_magnitudes[i],1) 
    upward_transition_points[i] = maxima(backward_magnitudes[i],1) 
    downward_transition_frequencies[i] = (frequency_range[downward_transition_points[i]]+frequency_range[downward_transition_points[i]+1])/2 #since the slope is calculated between two data points, take the middle between the two corresponding frequencies
    upward_transition_frequencies[i] = (frequency_range[-1-upward_transition_points[i]]+frequency_range[-2-upward_transition_points[i]])/2 #since the slope is calculated between two data points, take the middle between the two corresponding frequencies, the frequency range is reversed for the backwards sweep

for i in range(sweep_count):
    plt.axvline(downward_transition_frequencies[i], ymin=0,ymax=1)
    plt.axvline(upward_transition_frequencies[i], ymin=0,ymax=1,color='r')