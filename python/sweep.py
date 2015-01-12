import visa
import matplotlib.pyplot as plt
import numpy as np

##parameters
center_frequency = 4607000
frequency_span = 2000
bandwidth = 300
data_points = 201
sweep_count = 1
minimum_power = 0
maximum_power = 0

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

#data initialization

amplitudes = np.zeros([sweep_count,2*data_points])
amplitudes_real = np.zeros([sweep_count,data_points])
amplitudes_imaginary = np.zeros([sweep_count,data_points])
magnitudes = np.zeros([sweep_count,data_points])

power = np.linspace(minimum_power,maximum_power,sweep_count)

for i in range(sweep_count):
    inst.write('POWE '+str(power[i]))
    
    #measurement
    inst.write('CLES') # clear all status registers
    inst.write('*SRE 4;ESNB 1') #sets interrupt on sweep end
    inst.write('SING')
    inst.wait_for_srq()
    
    #print to NA screen
    inst.write('AUTO') #automatically scales data
    
    #processing 
    inst.write('CIRF LIN') #set data format
    amplitudes = inst.query_ascii_values('OUTPDATA?')
    amplitudes_real[i] = np.array(amplitudes[::2])
    amplitudes_imaginary[i] = np.array(amplitudes[1::2])
    magnitudes[i] = np.sqrt(np.multiply(amplitudes_real[i], amplitudes_real[i]) + np.multiply(amplitudes_imaginary[i], amplitudes_imaginary[i])) #quadratic sum of imaginary and real terms
    inst.write('CLES') # clear all status registers
    
    #print to computer screen
    plt.plot(magnitudes[i])
    
np.save('test_real', amplitudes_real)
np.save('test_imaginary',amplitudes_imaginary)
np.save('test_magnitudes',magnitudes)

def minima(data, n):
    arguments = np.zeros(n)
    slope = np.diff(data)
    for i in range(0,n):
        arguments[i] = np.argmin(slope)
        slope[arguments[i]] = 0
    return arguments
    
A = np.load('test_magnitudes.npy')
minima(A[0],1)
plt.axvline(minima(A[0],1), ymin=0,ymax=max(A[0]),color='r')