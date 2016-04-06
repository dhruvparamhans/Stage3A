import os 
import fnmatch 
import numpy as np 
from scipy.signal import savgol_filter
import matplotlib.pyplot as plt


DATA_PATH = '/home/dhruv/Documents/Stage3A/Data'

def get_data(filename):
	with open(filename, 'r') as f:
		data_list = [line.split() for line in f]
	ch1 = [int(x[0]) for x in data_list]
	ch2 = [int(x[1]) for x in data_list]
	return ch1, ch2

def mirrored(maxval, inc):
	return np.linspace(-maxval, maxval, 2*maxval // inc)

def write2file(filename, *args):
	x = zip(*args)
	with open(filename, 'w-') as f:
		for t in x:
			line  = ' '.join(str(w) for w in t)
			f.write(line + '\n')
	print "Written data to file : {}\n".format(filename)

def clip_and_smooth(raw, cutoff1, cutoff2, set_offset=False, offset=3, max_freq = 384.2390, min_freq = 384.2230, mid_freq = 384.231, resolution=16./1197):
	## Remove the data which is not required for fit. 
	## Usually corresponds to the begin of the scan 
	## Will need to be changed once we trigger the scan with the signal from the laser 
	if set_offset:
		temp = raw[cutoff1+offset:cutoff2]
	else:
		temp = raw[cutoff1:cutoff2]
	#max_freq = max_freq - (resolution*cutoff/1000)
	max_freq_detuned = 7.0
	min_freq_detuned = -7.0
	step = (max_freq_detuned - min_freq_detuned)/len(temp)
	#mid_freq_temp = (max_freq+min_freq_temp)/2
	#print mid_freq_temp
	freqs = np.arange(min_freq_detuned, max_freq_detuned, step)
	## Baseline correction
	# def baseline(x):
	# 	return x*(temp[1] - temp[0]) + temp[0]
	baseline = lambda x: x*((np.max(temp)-temp[0])/(1.0*len(temp))) + temp[0]
	temp = np.asarray(temp)/baseline(np.asarray(range(len(temp))))
	smoothed = savgol_filter(temp,3,1)
	smoothed -= np.min(smoothed)
	smoothed /= np.max(smoothed)
	return freqs, smoothed, list(reversed(smoothed))

def find_files(directory, pattern):
	"""
	Function to recursively find files with a given extension 
	within a given directory
	"""
	for root, dirs, files in os.walk(directory):
		for basename in files:
			if fnmatch.fnmatch(basename, pattern):
				filename = os.path.join(root, basename)
				yield filename

