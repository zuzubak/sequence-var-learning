import matplotlib.pyplot as plt
from scipy.io import wavfile
import numpy as np
import evfuncs
from pydub import AudioSegment
import string
import random

###modified from https://stackoverflow.com/questions/47147146/save-an-image-only-content-without-axes-or-anything-else-to-a-file-using-matl
def graph_spectrogram(wav_file,directory,ID='no_ID'):
    rate, data = wavfile.read(wav_file)
    fig,ax = plt.subplots(1)
    fig.subplots_adjust(left=0,right=1,bottom=0,top=1)
    ax.axis('off')
    pxx, freqs, bins, im = ax.specgram(x=data, Fs=rate, noverlap=384, NFFT=512)
    ax.axis('off')
    fig.savefig(directory+'spectrograms/'+ID+'.png', dpi=300, frameon='false')

def get_syls(directory,prepad=10,postpad=10,shuffle=True,n=50, notbatch='notbatch'):
    notmat_lines_list = list(open(directory+notbatch))
    notmat_list = [directory+value[:value.index('\n')] for value in notmat_lines_list]
    if shuffle==True:
        random.shuffle(notmat_list)
    spectrograms_created = 0
    f=0
    for file in notmat_list:
        ndict = evfuncs.load_notmat(file)
        wav_file = file.strip('.not.mat')
        file_audio = AudioSegment.from_wav(wav_file)
        i=0
        for syl in ndict['labels']:
            if syl in string.ascii_letters and spectrograms_created < n:
                onset=ndict['onsets'][i]
                offset=ndict['offsets'][i]
                syl_snippet = file_audio[onset-prepad:offset+postpad]
                ID = str(f)+'_'+str(i)
                snippet_filename = directory+'snippets/'+ID+'.wav'
                syl_snippet.export(snippet_filename,format='wav')
                graph_spectrogram(snippet_filename,directory,ID=ID)
                i+=1
                spectrograms_created += 1
        f+=1

        
