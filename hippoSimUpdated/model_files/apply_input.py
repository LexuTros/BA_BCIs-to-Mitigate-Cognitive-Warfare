#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import scipy
from scipy import signal
from brian2 import *
import ast

def lecture(filename):
    data_array=[]
    file=open(filename,'r')
    for data in file :
        d=ast.literal_eval(data[:-1])
        data_array.append(d)
    file.close()
    return data_array
  

def ecriture(filename,data,tmin,dur):
    record_dt=1./1024 *second
    start_ind=int(tmin/record_dt)
    end_ind=int(start_ind+dur/record_dt)
    
    time_series=open(filename,'w')
    time_series.write('[')
    for n in data[start_ind:end_ind]:
        time_series.write('%.2E,'%n)
    time_series.write(']\n')
    time_series.close()
    

def get_FR(sig,fs):
    N=2
    nyq = 0.5 * fs
    low = 3 / nyq
    high=50/nyq
    b, a = scipy.signal.butter(N, high, btype='low') 
        
    sig_filt=scipy.signal.filtfilt(b,a,sig)

    sig_envelope=abs(sig_filt)
    
    sig_noised=5/6*sig_envelope+max(sig_envelope)/6*rand(len(sig_envelope))
    
    return sig_noised

def normalize(sig1,sig2,sig3,record_dt,maxFR):
        MMM=max((max(sig1),max(sig2),max(sig3)))
#        sig1=200*sig1/MMM
#        sig2=200*sig2/MMM
#        sig3=200*sig3/MMM
        sig1=maxFR*sig1/max(sig1)
        sig2=maxFR*sig2/max(sig2)
        sig3=maxFR*sig3/max(sig3)
        sig1=TimedArray(sig1*Hz,dt=record_dt)
        sig2=TimedArray(sig2*Hz,dt=record_dt)
        sig3=TimedArray(sig3*Hz,dt=record_dt) 
        return sig1,sig2,sig3
    
def timedarray2array(t_array,tmax,dt):
    t,ind=0*second,0
    res_array=zeros((int(tmax/dt),1))
    while t<tmax:
        res_array[ind]=t_array(t)
        t+=dt
        ind+=1
    return res_array

def apply_input(input_type,A0,A1,dur,f1,duty_cycle,runtime,in_file_1,in_file_2,in_file_3,in_fs):
    record_dt=1./1024 *second
#    print(input_type,A0,A1,dur,f1,runtime)
    global inputs1,inputs2,inputs3
    #calcul des inputs
    if input_type=='custom':
        input_1=lecture(in_file_1)
        input_2=lecture(in_file_2)
        input_3=lecture(in_file_3)
         

        inputs_FR_1=get_FR(input_1,in_fs/Hz)
        inputs_FR_2=get_FR(input_2,in_fs/Hz)
        inputs_FR_3=get_FR(input_3,in_fs/Hz)
    
        inputs1,inputs2,inputs3=normalize(inputs_FR_1,inputs_FR_2,inputs_FR_3,1./in_fs,200)
        

    elif input_type=='square':
        T1=int(2*int(1/f1/record_dt)*duty_cycle)
        T2=int(2*int(1/f1/record_dt)*(1-duty_cycle))
        in_1=array([0.]*int(runtime/record_dt))
        deb=int(250*msecond/record_dt)
        count=1
        T=T1
#        print(deb,T,len(in_1), A0, A1)

        while deb+T<=int((250*msecond+dur)/record_dt):
            if count==0:
                in_1[deb:deb+T]=A0
            else :
                in_1[deb:deb+T]=A1
            #print(in_1[deb])
            deb=deb+T
            count=(count+1)%2
            if count==0:
                T=T2
            else :
                T=T1
        in_1[deb:int((250*msecond+dur)/record_dt)]=A0*int(count==0)+A1*int(count==1)
#        figure()
#        plot(in_1)
        print(in_1)
        inputs1=TimedArray(in_1*namp,dt=record_dt)
        inputs2=TimedArray(in_1*namp,dt=record_dt)
        inputs3=TimedArray(in_1*namp,dt=record_dt)
        

#    array_in1=timedarray2array(inputs1,60*second,record_dt)
#    array_in2=timedarray2array(inputs2,60*second,record_dt)
#    array_in3=timedarray2array(inputs3,60*second,record_dt)
#    figure()
#    subplot(311)
#    plot(array_in1)
#    subplot(312)
#    plot(array_in2)
#    subplot(313)
#    plot(array_in3)
    return inputs1,inputs2,inputs3
