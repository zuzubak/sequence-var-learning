import numpy as np
import scipy.io.wavfile as wave
import python_speech_features as psf
from pydub import AudioSegment

def convert(path):

    #open file (supports all ffmpeg supported filetypes) 
    audio = AudioSegment.from_file(path, path.split('.')[-1].lower())

    #set to mono
    audio = audio.set_channels(1)

    #set to 44.1 KHz
    audio = audio.set_frame_rate(44100)

    #save as wav
    audio.export(path, format="wav")

def getSpectrogram(path, winlen=0.025, winstep=0.01, NFFT=512):

    #open wav file
    (rate,sig) = wave.read(path)

    #get frames
    winfunc=lambda x:np.ones((x,))
    frames = psf.sigproc.framesig(sig, winlen*rate, winstep*rate, winfunc)

    #Magnitude Spectrogram
    magspec = np.rot90(psf.sigproc.magspec(frames, NFFT))

    #noise reduction (mean substract)
    magspec -= magspec.mean(axis=0)

    #normalize values between 0 and 1
    magspec -= magspec.min(axis=0)
    magspec /= magspec.max(axis=0)

    #show spec dimensions
    print(magspec.shape)

    return magspec