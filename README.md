# Senior_Project-Auto_Accompaniment_System
## This accompaniment system is designed to work on Raspberry Pi with [PyAudio](https://people.csail.mit.edu/hubert/pyaudio/ "PyAudio Webpage").
### main.py
The main.py controls the overall accompaniment system. Most of modules will be loaded by main.py

### corr.py
The corr.py takes audio file and will return the time(seconds) which has the highest auto correlation value.

### rec_audio.py
The rec_audio.py records sound from microphone. *Some settings might be changed according to a device*.
