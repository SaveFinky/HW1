#  FINCATO SAVERIO 1229082
#  Reti di Calcolatori - Homework 1
#  VOICE ACTIVITY DETECTION
import struct
import cmath
#python3 -m pip install numpy   if you don't have NumPy
import numpy as nmp
from numpy.fft import fft
import os
import sys

# PARAMETERS
frame_duration= 20 #ms
N_samples = 160 #number of semples in 20ms 

def VAD_Method(i_file,o_file):
    
    loop=True
    while loop:
        samples = [0] * N_samples
        raw = [0] * N_samples

        try:
            for i in range(N_samples):#160 saples x iter
                raw[i] = i_file.read(1)
                samples[i] = float(struct.unpack('B', raw[i])[0])

                if samples[i] > 127: samples[i] = (256-samples[i])*(-1) #to signed int
        except:
            loop=False #end of input

        y = fft(samples)#Fast Fourier Transformate to convert a signal into
        #                individual spectral components and provide frequency
        
        for i in range(len(y)):
            y[i] = cmath.sqrt(y[i].real**2+y[i].imag**2) #amplitude

        #if the signal amplitude is contained in [200,3400] it is classified as voice
        if(nmp.amax(y) > 200 and nmp.amax(y) <= 3400):
            #ACTIVE
            print("1",end='')
            for i in range(N_samples):
                o_file.write(raw[i])
        
        else:
            #INACTIVE
            print("0",end='')
            for i in range(N_samples):
                o_file.write(b'\x00')

    print()        
    o_file.close()
    i_file.close()


# MAIN
if len(sys.argv)== 1 or str(sys.argv[1])=="1" :

#Prof input files ---------------------------------
    print("FIRST MODE")
    for i in range(1,6):
        o_file = open("outputVAD"+str(i) + ".data", "wb") #bytes stream
        i_file = open("inputaudio"+str(i) + ".data", "rb")
        print("\nFile n:"+str(i))
        VAD_Method(i_file,o_file)

#--------------------------------------------------

else :
    if str(sys.argv[1])=="2" :
        #new file required
        #INPUT
        print("SECOND MODE")
        while True:
            input_name = input("Enter the name of inputfile (with .data): ")
            if (os.path.splitext(input_name)[1] == ".data") :
                try:
                    i_file = open(input_name, "rb")
                    break
                except Exception as e: 
                    print(str(e)+"- while opening the file, check and reinsert")
                
            else :
                print("\n!missing or wrong extension, repeat")

        #OUTPUT
        while True:
            output_name = input("Enter the name of outputfile (with .data): ")
            if (os.path.splitext(output_name)[1] == ".data") :
                try:
                    o_file = open(output_name, "wb")
                    break
                except Exception as e: 
                    print(str(e)+"- while opening the file, check and reinsert")
                
            else :
                print("\n!missing or wrong extension, repeat")
        
        print("\n" + input_name + " --VAD--> " + output_name)
        VAD_Method(i_file,o_file)

    else:
        #OTHER MODE
        print("Mode '"+str(sys.argv[1]) +"' does not exist")

