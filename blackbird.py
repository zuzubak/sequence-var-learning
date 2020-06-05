from scipy.io.wavfile import write
from scipy.signal import buttord, butter, filtfilt
from scipy.stats import norm
from numpy import int16
from scipy import signal
import numpy as np
from matplotlib import pyplot as plt
from scipy.io import wavfile


def trim(signal, samp_rate): #from https://www.johndcook.com/blog/2016/04/27/how-to-create-green-noise-in-python/
    # start and stop of green noise range
    left = 1500 # Hz
    right = 5600 # Hz

    nyquist = (samp_rate/2)
    left_pass  = 1.1*left/nyquist
    left_stop  = 0.9*left/nyquist
    right_pass = 0.9*right/nyquist
    right_stop = 1.1*right/nyquist

    (N, Wn) = buttord(wp=[left_pass, right_pass],
                      ws=[left_stop, right_stop],
                      gpass=2, gstop=30, analog=0)
    (b, a) = butter(N, Wn, btype='band', analog=0, output='ba')
    return filtfilt(b, a, signal)

def to_integer(signal): #from https://www.johndcook.com/blog/2016/04/27/how-to-create-green-noise-in-python/
    # Take samples in [-1, 1] and scale to 16-bit integers,
    # values between -2^15 and 2^15 - 1.
    signal /= max(signal)
    return int16(signal*(2**15 - 1))

def make_noise(signal=None, N = 44100):
    white_noise= norm.rvs(0, 1, 3600*N) # three seconds of audio
    if signal.any()==None:
        signal = white_noise
    blackbirdify = trim(signal, N)
    write("blackbird_noise.wav", N, to_integer(blackbirdify))

def get_psd(wav_file):
    rate, data = wavfile.read(wav_file)
    mono_data = []
    for item in data:
        mono_data.append(item[0])
    freqs, psd = signal.welch(mono_data,rate)
    plt.figure(figsize=(5, 4))
    plt.semilogx(freqs, psd)
    plt.title('PSD: power spectral density')
    plt.xlabel('Frequency')
    plt.ylabel('Power')
    plt.tight_layout()
    plt.show()
