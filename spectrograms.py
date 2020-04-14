import matplotlib.pyplot as plt
import matplotlib
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


###modified from https://stackoverflow.com/questions/47147146/save-an-image-only-content-without-axes-or-anything-else-to-a-file-using-matl
def graph_spectrogram(wav_file,directory,ID='no_ID'):
    rate, data = wavfile.read(wav_file) #convert wav file to raw audio data
    fig,ax = plt.subplots(1) #create a new subplot within the matplotlib figure, to house the spectrogram
    fig.patch.set_visible(False) #get rid of white space around spectrograms -- from https://stackoverflow.com/questions/14908576/how-to-remove-frame-from-matplotlib-pyplot-figure-vs-matplotlib-figure-frame
    ax.axis('off') #turn off x (time) and y (frequency) axes
    pxx, freqs, bins, im = ax.specgram(x=data, Fs=rate, noverlap=511, NFFT=512)
    ax.set_ylim([0,10000])
    fig.set_size_inches(len(data)/12000,1) #scale the figure by the length (in time) of the audio sample being plotted, so that output images for longer samples are wider.
    plt.savefig(directory+'spectrograms/'+ID+'.png', dpi=400, frameon=False)

def graph_spectrogram2(wav_file,directory,ID='no_ID'):
    fs, x = wavfile.read(wav_file)
    f, t, Sxx = signal.spectrogram(x, fs)
    plt.pcolormesh(t, f[0:20], Sxx[0:20])
    plt.show()

def get_syls(directory,prepad=20,postpad=20,shuffle=True,n=50, notbatch='notbatch'):
    for fp in [directory+'snippets', directory+'spectrograms']:
        if os.path.exists(fp):
            for file in os.listdir(fp):
                os.remove(fp+'/'+file)
            os.rmdir(fp)
        os.makedirs(fp)
    notmat_lines_list = list(open(directory+notbatch)) #extract a list of labelled songfiles
    notmat_list = [directory+value[:value.index('\n')] for value in notmat_lines_list] #extract a list of labelled songfiles
    if shuffle==True: #randomize the order in which the files are processed, if the parameter "shuffle" is set to True
        random.shuffle(notmat_list)
    spectrograms_created = 0 #keeps a count of how many spectrograms have been generated
    f=0 #keeps track of how many songfiles have been processed
    for file in notmat_list:
        ndict = evfuncs.load_notmat(file) #loads variables stored in the notmat file pertaining to the current songfile
        wav_file = file.strip('.not.mat') #the wav file corresponding to the current notmat file should be the same, minus the ".not.mat" at the end
        file_audio = AudioSegment.from_wav(wav_file) #create an AudioSegment object of the relevant wave file, so that it can be sliced up.
        i=1 #keeps track of how many spectrograms have been generated for the current songfile
        for syl in ndict['labels']: #iterate through the labelled syllable tokens in the songfile
            if syl in string.ascii_letters and spectrograms_created < n: #check that the current syllable is a letter of the alphabet (so that "-" and "0" will be ignored)
                try:
                    onset=ndict['onsets'][i] #retrieve the onset time (in milliseconds) of the syllable within the file
                    offset=ndict['offsets'][i]
                    syl_snippet = file_audio[onset-prepad:offset+postpad] #create an AudioSegment that begins "prepad" ms before the syllable begins, and ends "postpad" milliseconds after it ends, where those two parameters are specified by the user.
                    ID = str(f)+'_'+str(i) #create an arbitrary ID for the current syllable, by concatenating the number of songs that have been processed and the number of syllables processed in the current song, with an underscore in between.
                    snippet_filename = directory+'snippets/'+ID+'.wav'
                    syl_snippet.export(snippet_filename,format='wav')
                    graph_spectrogram(snippet_filename,directory,ID=ID)
                    i+=1
                    spectrograms_created += 1
                except BaseException:
                    pass
        f+=1

        
def make_pptx(directory,fname='for_categorization.pptx', border_width_inches=0.01, buffer_width_inches=0.01):
    prs = Presentation()
    title_slide_layout = prs.slide_layouts[6] #blank slide
    slide = prs.slides.add_slide(title_slide_layout)
    shapes = prs.slides[0].shapes
    left = top = Inches(border_width_inches)
    spectrograms_dir = directory + 'spectrograms/'
    files_list = os.listdir(spectrograms_dir)
    i=0
    for spectrogram in files_list:
        spec_fp = spectrograms_dir + spectrogram
        if 'png' in spec_fp:
            try:
                picture = shapes.add_picture(spec_fp, left, top)
                image_width = Inches(picture.image.size[0]/picture.image.dpi[0])
                image_height = Inches(picture.image.size[1]/picture.image.dpi[1])
                #left += Inches(buffer_width_inches)
                if left + 2*image_width > prs.slide_width:
                    if top + image_height < prs.slide_height: #Create new line if adding image to current line will exceed slide borders.
                        left = Inches(border_width_inches)
                        top += image_height
                    else:
                        break
                else:
                    left += image_width
                i+=1
            except BaseException:
                pass
    prs.save(directory+fname)

def batch_slides(directory):
    for bird_directory in os.listdir(directory):
        if '.' not in bird_directory:
            get_syls(directory+bird_directory+'/')
            make_pptx(directory+bird_directory+'/')

def sample_size(directory,ss_list = [30,50,75,100,150]):
    for bird_directory in os.listdir(directory):
        if '.' not in bird_directory:
            for ss in ss_list:
                get_syls(directory+bird_directory+'/', n=ss)
                make_pptx(directory+bird_directory+'/', fname=str(ss)+'_categorization.pptx')