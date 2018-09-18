# Introduction

This library is for data that is arranged as follows (in the form of lists - this is just for visual understanding):

|id| Timestamp|values|
| ------ | ------ | ------- |
| 1 | 2018:06:05 03:02:00| 2.3|
| 2 | 2018:06:05 03:04:33| 2.4|
| 3 | 2018:06:05 03:07:01|3.3
| 4 | 2018:08:03 03:07:55 | 2.9
| 5 | 2018:08:03 03:08:44 | 3.3
| 6 | 2018:08:03 03:12:12  | 2.4

As you can see, the above signal is *a non uniformly sampled signal* as observed by the irregularly spaced timestamps.
You can apply several functions of this libary to the above data suach as:
```python
from signal_processing import signal_processing as sp
upsampled_signal = sp.upsampling(input_signal,5) # Does upsampling by a factor of 5
downsampled_signal = sp.downsampling(upsampled_signal,3) # Does downsampling by a factor of 3
sampled_signal = sp.sampling_non_uniformly_sampled_signals(input_signal,freq_in_minutes) # samples the signal on a              frequency of given minutes 
```
# Installation 
```python
pip install signal-processing
```
