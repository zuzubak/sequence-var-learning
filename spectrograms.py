import matplotlib.pyplot as plt
from scipy.io import wavfile
import numpy as np
import evfuncs
from pydub import AudioSegment
import string

###modified from https://stackoverflow.com/questions/47147146/save-an-image-only-content-without-axes-or-anything-else-to-a-file-using-matl
def graph_spectrogram(wav_file,directory):
    rate, data = wavfile.read(wav_file)
    fig,ax = plt.subplots(1)
    fig.subplots_adjust(left=0,right=1,bottom=0,top=1)
    ax.axis('off')
    pxx, freqs, bins, im = ax.specgram(x=data, Fs=rate, noverlap=384, NFFT=512)
    ax.axis('off')
    fig.savefig(directory+'snippets/wav_file+'.png', dpi=300, frameon='false')

def get_syls(notbatch,directory,prepad=10,postpad=10):
    notmat_name_list = list(open(directory+notbach))
    notmat_list = [directory+value for value in notmat_name_list]
    for file in notmat_list:
        ndict = evfuncs.load_notmat(file)
        wav_file = file.strip('.not.mat')
        file_audio = AudioSegment.from_wav(wav_file)
        i=0
        for syl in ndict.labels:
            if syl in string.ascii_letters:
                onset=ndict.onsets[i]
                offset=ndict.offsets[i]
                syl_snippet = file_audio[onset-prepad:offset+postpad]
                snippet_filename = './snippets/'+wav_file+str(i)'.wav'
                syl_snippet.export(snippet_filename,format='wav')
                graph_spectrogram(syl_snippet,directory)

        
