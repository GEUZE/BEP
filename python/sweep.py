import visa
import matplotlib.pyplot as plt
import numpy 

#connect to NA
rm = visa.ResourceManager()
#print(rm.list_resources())
inst = rm.open_resource('GPIB0::17::INSTR')
#print(inst.query('*IDN?'))

#initialization

inst.write('CENT 4607000')  #\set the frequency range of the sweep
inst.write('SPAN 2000')     #/
inst.write('BWAUTO OFF')    #\set the IF bandwidth
inst.write('BW 1000')        #/
inst.write('FMT LINM')  #set NA screen format
inst.write('POIN 201')  #set number of points

data_points = 1
minimum_power = 0
maximum_power = 0
for x in range(minimum_power, ):
    inst.write('POWE '+str(x))
    
    #measurement
    inst.write('CLES') # clear all status registers
    inst.write('*SRE 4;ESNB 1') #sets interrupt on sweep end
    inst.write('SING')
    inst.wait_for_srq()
    
    #print to NA screen
    inst.write('AUTO') #automatically scales data
    
    #processing
    amplitudes_real = zeros(
    inst.write('CIRF LIN') #set data format
    amplitudes = inst.query_ascii_values('OUTPDATA?')
    amplitudes_real[x] = numpy.array(amplitudes[::2])
    amplitudes_imaginary[x] = numpy.array(amplitudes[1::2])
    magnitudes[x] = numpy.sqrt(numpy.multiply(amplitudes_real[x], amplitudes_real[x]) + numpy.multiply(amplitudes_imaginary[x], amplitudes_imaginary[x])) #quadratic sum of imaginary and real terms
    inst.write('CLES') # clear all status registers
    
#print to computer screen
    plt.plot(magnitudes)