import visa
import matplotlib.pyplot as plt
import numpy 

##parameters
center_frequency = 4607000
frequency_span = 2000
bandwidth = 1000
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
inst.write('SPAN '+str(frequency_span))     #/
inst.write('BWAUTO OFF')    #\set the IF bandwidth
inst.write('BW '+str(bandwidth))        #/
inst.write('FMT LINM')  #set NA screen format
inst.write('POIN '+str(data_points)  #set number of points

#data initialization

amplitudes = numpy.zeros([sweep_count,2*data_points])
amplitudes_real = numpy.zeros([sweep_count,data_points])
amplitudes_imaginary = numpy.zeros([sweep_count,data_points)]

power = linspace(minimum_power,maximum_power,sweep_count)

for i in range(sweep_count):
    inst.write('POWE '+str(power(i)))
    
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
    amplitudes_real[i] = numpy.array(amplitudes[::2])
    amplitudes_imaginary[i] = numpy.array(amplitudes[1::2])
    magnitudes[i] = numpy.sqrt(numpy.multiply(amplitudes_real[i], amplitudes_real[i]) + numpy.multiply(amplitudes_imaginary[i], amplitudes_imaginary[i])) #quadratic sum of imaginary and real terms
    inst.write('CLES') # clear all status registers
    
#print to computer screen
    plt.plot(magnitudes[i])
