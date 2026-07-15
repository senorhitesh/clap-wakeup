import sounddevice as sd
from scipy.io.wavfile import write
from application_open import run_appication
import librosa
# parameters
fs = 4000
duration = 0.03
channel = 1

while True:
    audio = sd.rec(
        int(fs* duration),
        samplerate=fs,
        channels=channel,
        dtype="float32"
    )
    sd.wait()
    pitch,_,_ = librosa.pyin(audio.flatten(), fmin=50, fmax=1500)
    print(pitch)

    if(pitch > 1000):
        run_appication()
        break

