import sys as sys
import matplotlib.pyplot as plt
import matplotlib
from matplotlib import cm
from scipy.io import wavfile
import numpy as np
import evfuncs
from pydub import AudioSegment
import string
import random
from scipy import signal
from pptx import Presentation
from pptx.util import Inches
import os
import csv
import math
import time
import scipy.io

def make_spectrogram(wav_file):
    rate, data = wavfile.read(wav_file) #convert wav file to raw audio data
    fig,ax = plt.subplots(1) #create a new subplot within the matplotlib figure, to house the spectrogram
    fig.patch.set_visible(False) #get rid of white space around spectrograms -- from https://stackoverflow.com/questions/14908576/how-to-remove-frame-from-matplotlib-pyplot-figure-vs-matplotlib-figure-frame
    ax.axis('off') #turn off x (time) and y (frequency) axes
    pxx, freqs, bins, im = ax.specgram(x=data, Fs=rate, noverlap=511, NFFT=512,cmap=cm.jet, scale='dB')
    ax.set_ylim([0,10000])
    fig.set_size_inches(len(data)/2400,5) #scale the figure by the length (in time) of the audio sample being plotted, so that output images for longer samples are wider.
    text_box = matplotlib.widgets.TextBox(ax,'Enter label:')
    text_box.on_submit(submit)
    plt.show()
    return {'ax':ax,'fig':fig,'pxx':pxx}

def submit(input_str):
    global label
    label = input_str

directory=sys.argv[1]

songs_dict = {}

label = '-'

notmat_lines_list = list(open(directory+'notbatch')) #extract a list of labelled songfiles
notmat_list = [directory+value[:value.index('\n')] for value in notmat_lines_list] #extract a list of labelled songfiles
spectrograms_created = 0 #keeps a count of how many spectrograms have been generated
f=0 #keeps track of how many songfiles have been processed
for file in notmat_list:
    if label == 'quit':
        break
    ndict = evfuncs.load_notmat(file) #loads variables stored in the notmat file pertaining to the current songfile
    wav_file = file.strip('.not.mat') #the wav file corresponding to the current notmat file should be the same, minus the ".not.mat" at the end
    file_audio = AudioSegment.from_wav(wav_file) #create an AudioSegment object of the relevant wave file, so that it can be sliced up.
    i=1 #keeps track of how many spectrograms have been generated for the current songfile
    #print(type(ndict['onsets']))
    if type(ndict['onsets']) is not int:
        indices = list(range(len(ndict['onsets'])))
        random.shuffle(indices)
        for i in indices: #iterate through the labelled syllable tokens in the songfile
            onset=ndict['onsets'][i] #retrieve the onset time (in milliseconds) of the syllable within the file
            offset=ndict['offsets'][i]
            syl_snippet = file_audio[onset-20:offset+20] #create an AudioSegment that begins "prepad" ms before the syllable begins, and ends "postpad" milliseconds after it ends, where those two parameters are specified by the user.
            ID = str(f)+'_'+str(i) #create an arbitrary ID for the current syllable, by concatenating the number of songs that have been processed and the number of syllables processed in the current song, with an underscore in between.
            snippet_filename = directory+'syl'+'.wav'
            syl_snippet.export(snippet_filename,format='wav')
            ax = make_spectrogram(snippet_filename)['ax']
            label = input('Syllable '+str(i)+' of '+str(len(ndict['onsets']))+' in '+file+'. Label:')
            if label == 'quit':
                break
            a=list(ndict['labels'])
            a[i] = label
            ndict['labels'] = ''
            for character in a:
                ndict['labels']+=character
            scipy.io.savemat(file,ndict)
            i+=1
    else:
        pass
print(ndict['labels'])