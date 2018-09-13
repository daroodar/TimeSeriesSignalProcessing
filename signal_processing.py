# -*- coding: utf-8 -*-
"""
Created on Thu Sep 13 11:51:23 2018

@author: osama

Python version: 2.7.12
"""

from __future__ import division #Because Python 2's division isn't supported for floats
import numpy as np
from copy import deepcopy
from datetime import timedelta


def down_sampling(input_signal,down_sample_factor,method='simple',index_values=2):
    ''' This function returns the downsampled signal by the factor given 
    Also, you can specify the method of downsampling
    My particular list was arranged as format of [some_id,time_stamp,values] 
    so that is why index of values is 2. If you have list element's format as 
    [time_stamp,value] then specify index_values as 1 '''

    input_signal=deepcopy(input_signal)    
    values=[row[index_values] for row in input_signal]
    down_sampled_simple=input_signal[0:len(input_signal):down_sample_factor]
    
    if (method=='simple'):
        down_sampled_signal=down_sampled_simple
        return down_sampled_simple
    
    subsets=[values[i:i+down_sample_factor] for i in range(0,len(values),down_sample_factor)]
    down_sampled_average=[round(np.mean(subsets[i]),7) for i in range(len(subsets))]
    down_sampled_max=[round(np.max(subsets[i]),7) for i in range(len(subsets))]
    
    if (method=='average'):
        for i in range(len(down_sampled_simple)):
            down_sampled_simple[i][index_values]=down_sampled_average[i]    
        down_sampled_signal=down_sampled_simple
        return down_sampled_signal
        
    if (method=='max'):
        for i in range(len(down_sampled_simple)):
            down_sampled_simple[i][index_values]=down_sampled_max[i]    
        down_sampled_signal=down_sampled_simple
        return down_sampled_signal
        

def sampling_non_uniformly_sampled_signals(input_signal,freq_in_minutes,index_systemid=0,index_timestamp=1,index_values=2):
''' This function is for sampling non uniformly sampled signals '''
    sampled_signal=[]
    timestamp_array=np.asarray(input_signal)[:,1]
    signal_freq=determine_frequency(timestamp_array)
    system_id=input_signal[0][index_systemid]
    if (signal_freq==-1):
        pass
    else:
        print("It is already uniformly sampled with a frequency of "+str(signal_freq))
        return -1
    time_start=round_datetime_to_nearest_minutes(timestamp_array[0],freq_in_minutes,'round_down')
    time_end=round_datetime_to_nearest_minutes(timestamp_array[len(timestamp_array)-1],freq_in_minutes,'round_up')
    times_list=date_linspace_freq(time_start,time_end,freq_in_minutes)
    for i in range(len(times_list)-1):
        result_in_between=extract_values_in_between_timestamps(times_list[i],times_list[i+1],input_signal)
        sampled_signal.append([system_id,times_list[i],result_in_between])
    
    return sampled_signal        




def up_sampling(input_signal,up_sample_factor,method='repeat',index_timestamp=1,index_values=2):
    ''' This function returns the upsampled signal where you have timestamps and some values across them.
    My particular list was arranged as format of [some_id,time_stamp,values] so that is why index of time stamp is 1 
    and index of values is 2. If you have list element's format as [time_stamp,value] then specify index_timestamp as 0 and
    index_values as 1
    You can also specify the method for upsampling'''
    
    input_signal=deepcopy(input_signal)
    repeated_signal=[input_signal[i//up_sample_factor] for i in range(len(input_signal)*up_sample_factor)]
    for x in range(up_sample_factor-1):
        repeated_signal.pop()
    Temp_time=[]
    Temp_values=[]
    
    if(method=='repeat'):
        for i in range(len(input_signal)-1):
            Temp_time.append(date_linspace_steps(input_signal[i][index_timestamp],input_signal[i+1][index_timestamp],up_sample_factor))

        Temp_time = np.concatenate(Temp_time).ravel().tolist()
        Temp_time.append(input_signal[len(input_signal)-1][index_timestamp])
        
        result=[]
        for i in range(len(repeated_signal)):
            result.append([repeated_signal[i][0],Temp_time[i],repeated_signal[i][index_values]])
        
    elif(method == 'average'):
        for i in range(len(input_signal)-1):
            Temp_time.append(date_linspace_steps(input_signal[i][index_timestamp],input_signal[i+1][index_timestamp],up_sample_factor))
            values_to_append=np.linspace(input_signal[i][index_values],input_signal[i+1][index_values],up_sample_factor+1)
            values_to_append=values_to_append[:len(values_to_append)-1]
            Temp_values.append(values_to_append)
        Temp_time = np.concatenate(Temp_time).ravel().tolist()
        Temp_time.append(input_signal[len(input_signal)-1][index_timestamp])
        
        Temp_values = np.concatenate(Temp_values).ravel().tolist()
        Temp_values.append(input_signal[len(input_signal)-1][index_values])
        
        result=[]
        for i in range(len(repeated_signal)):
            result.append([repeated_signal[i][0],Temp_time[i],Temp_values[i]])
    
    return result

 
def determine_frequency(input_signal):
    ''' This function determines the frequency of DATETIME signal(only) and tells if the input signal
    is not uniformly sampled, otherwise returns the frequency ..'''
    
    
    first_freq=input_signal[1]-input_signal[0]
    for i in range(0,len(input_signal)-1):
        if ((input_signal[i+1]-input_signal[i])!=first_freq):
            print("Input signal not uniformly sampled!")
            return -1
    return first_freq.seconds/60
    
    
        
def round_datetime_to_nearest_minutes(input_time,nearest_minutes,method='threshold_based'):
    ''' This function rounds datetime to nearest_minutes 
    for example 2018-06-05 22:55:47 will round off to 2018-06-05 23:00:00 if given 
    nearest_minutes is 10
    Also specify method as rounded_up if you always want rounded up output datetime'''
    
    rounded_time=deepcopy(input_time)
    minute=input_time.minute
    remainder=minute % nearest_minutes
    is_greater=remainder>=nearest_minutes/2
    
    if (method =='round_up'):
        rounded_minute=(minute-remainder+nearest_minutes)
    elif(method=='round_down'):
        rounded_minute=minute-remainder
    else:
        if(is_greater):
            rounded_minute=(minute-remainder+nearest_minutes)
        else:
            rounded_minute=minute-remainder
            
    minute_difference=rounded_minute-minute
    minute_difference_timedelta=timedelta(minutes=minute_difference)

    rounded_time=rounded_time+minute_difference_timedelta
    rounded_time=rounded_time.replace(second=0,microsecond=0)

    return rounded_time
    
    
    
def date_linspace_steps(start, end, steps):
    ''' This function performs a similar task such as np.linspace for 
    datetime functions 
    IF STEPS ARE TO BE SPECIFIED USE THIS FUNCTION 
    IF FREQUENCY IS TO BE SPECIFIED USE date_linspace_freq'''
    
    delta = (end - start) // steps
    increments = range(0, steps) * np.array([delta]*steps)
    return start + increments
    
    
    
def date_linspace_freq(start, end, freq):
    ''' This function performs a similar task such as np.linspace with frequency
    ,NOT STEPS
    freq is in minutes'''
    
    n=int((end-start).seconds/60)
    times_list = [start + timedelta(minutes=x) for x in range(0,n,freq)]
    return times_list
    
    
    
def extract_values_in_between_timestamps(start_time,end_time,times_list,method='average',index_timestamp=1,index_values=2):
    ''' This function will return all the valus that reside between the given times '''
    
    values_in_range=[]

    for i in range(len(times_list)):
        
        if (times_list[i][index_timestamp]>=end_time):
            
            if(method=='average'):  return np.mean(values_in_range)
            elif(method=='max'):    return max(values_in_range)

        if(times_list[i][index_timestamp]<start_time):
            continue
        
        else:
            # That means we are in between
            values_in_range.append(times_list[i][index_values])
            
            
    if (method=='average'): return np.mean(values_in_range)
    elif (method=='max'):   return max(values_in_range)
            
            

            
    


    
    