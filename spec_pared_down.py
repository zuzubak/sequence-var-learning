import matplotlib.pyplot as plt
import matplotlib
from scipy.io import wavfile
import numpy as np
import evfuncs
from pydub import AudioSegment
import string
import random
from scipy import signal

def graph_spectrogram(wav_file,directory,ID='no_ID'):
    rate, data = wavfile.read(wav_file) 
    fig,ax = plt.subplots(1)
    fig.patch.set_visible(False)
    ax.axis('off')
    pxx, freqs, bins, im = ax.specgram(x=data, Fs=rate, noverlap=511, NFFT=512)
    fig.set_size_inches(len(data)/3000,4)
    plt.savefig(directory+'spectrograms/'+ID+'.png', dpi=300, frameon=False)

    #aspect_ratio = 0.05/len(data)
    #plt.ylim(top=10000)
    #ax.axis('off')
    #ax.axis('off')
    #ax.set_adjustable('datalim')
    #ax.set_aspect(aspect_ratio)

