import sounddevice as sd
from application_open import run_appication
import librosa
import numpy
# parameters
fs = 16000 
threshold = 0.3
block  = 512  # ~32ms blocks, fine for RMS


def is_loud_transient(chunk, prev_rms, threshold):
    rms = numpy.sqrt(numpy.mean(chunk**2))
    jump =  rms - prev_rms
    return jump > threshold, rms

prev_rms = 0

with sd.InputStream(samplerate=fs, channels=1, blocksize=block) as stream:
    while True:
        chunk,_ = stream.read(block)
        print(chunk)
        chunk = chunk.flatten()
        print(chunk)
        triggered, prev_rms = is_loud_transient(chunk,prev_rms, threshold)
        print(triggered)
        print(prev_rms)
        if triggered:
            run_appication()
            break
