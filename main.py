# Load Modules
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
from __future__ import division

print "AUTO ACCOMPANIMENT SYSTEM WRITTEN BY JIHOON KIM"

# Load Reference Array
selection = raw_input('Select the song for accompaniment (A/B)')

while True:
	if selection = 'A' or 'a':
		reference = np.load('diff_A.npy')
		break
	elif selection = 'B' or 'b':
		reference = np.load('diff_B.npy')
		break
	else:
		print 'Wrong Input'


# Record a audio from a microphone
print 'START RECORDING'
record()

# Create Constant Q Fourier Transform
print 'Coverting Audio File to Chromagram'
F = Chromagram('output8.wav', nfft=16384, wfft=8192, nhop=2205)
print 'Coverting has been completed'

# Calculate Auto Correlation
print 'Calculating Maximum Correlation Time'
time = max_corr(reference,F)

# Playing Audio at the maximum correlation moment
tart = int((time+34))*2 #LR-CHANNEL
length = 30
CHUNK = 8192

tbp = wave.open('Full_B.wav','rb')
signal = tbp.readframes(-1)
signal = np.fromstring(signal,'Int16')
accom = pyaudio.PyAudio()

stream = accom.open(format=pyaudio.paInt16,channels = 2, output_device_index = 5, rate = tbp.getframerate(), output = True, frames_per_buffer = CHUNK)

pos = tbp.getframerate()*length
signal = signal[(start)*tbp.getframerate():(int(start)*tbp.getframerate())+pos]
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