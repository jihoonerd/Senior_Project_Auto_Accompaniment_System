# Load Modules
from __future__ import division

from bregman.suite import *
import os
import os.path
import numpy as np
import wave
import pyaudio
import sys
import struct

from pylab import *
from rec_audio import record
from corr import max_corr

print "AUTO ACCOMPANIMENT SYSTEM * WRITTEN BY JIHOON KIM"

print "DEMO SONG A: Cries and Whispers"
print "DEMO SONG B: B ROSSETTE"

# Load Reference Array
set_A = set(['A','a'])
set_B = set(['B','b'])

while True:
	selection = raw_input('Select the song for accompaniment (A/B): ')
	if selection in set_A:
		reference = np.load('diff_A.npy')
		ref_file = 'Acco_A.wav'
		print 'Song A is loaded.'
		break
	elif selection in set_B:
		reference = np.load('diff_B.npy')
		ref_file = 'Acco_B.wav'
		print 'Song B is loaded.'
		break
	else:
		print 'Wrong Input'

time_adjustment = raw_input('Enter the adjustment of the time from matching time: ')
time_adjustment = int(time_adjustment)
# System will use 'repeat' variable to decide whether the process will continue or not.
repeat = True
while repeat == True:

	# Record a audio from a microphone
	print 'START RECORDING'
	record()

	# Create Constant Q Fourier Transform
	print 'Coverting Audio File to Chromagram'
	F = Chromagram('sample.wav', nfft=16384, wfft=8192, nhop=2205)
	print 'Coverting has been completed.'

	# Calculate Auto Correlation
	print 'Calculating Maximum Correlation Time'
	time = max_corr(reference,F)

	# Playing Audio at the maximum correlation moment
	"""This part should be compensated according to calculation time of device."""
	time_compensation = 28
	start = int((time+time_adjustment))*2 + time_compensation #LR-CHANNEL
	length = 30
	CHUNK = 4096

	tbp = wave.open(ref_file,'rb')
	signal = tbp.readframes(-1)
	signal = np.fromstring(signal,'Int16')
	accom = pyaudio.PyAudio()

	stream = accom.open(format=pyaudio.paInt16, channels = 2, output_device_index = 5, rate = tbp.getframerate(), output = True, frames_per_buffer = CHUNK)

	pos = tbp.getframerate()*length
	signal = signal[start*tbp.getframerate():(start*tbp.getframerate())+pos]
	sig = signal[1:CHUNK]

	inc = 0
	data = 0

	while data != '':
	    data = struct.pack("%dh"%(len(sig)), *list(sig))
	    stream.write(data)
	    inc=inc+CHUNK
	    sig=signal[inc:inc+CHUNK]


	stream.close()
	accom.terminate()

	ask_repeat = raw_input('Do you want to proceed one more time? (y/n): ')
	yes = set(['Y','y'])
	no = set(['N','n'])

	while True:
		if ask_repeat in yes:
			repeat = True
			break
		elif ask_repeat in no:
			repeat = False
			break
		else:
			print 'Wrong Input'

print 'Done'