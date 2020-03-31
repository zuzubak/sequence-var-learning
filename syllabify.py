import evfuncs
from pydub import AudioSegment
import string
import random

def get_syls(bird_directory,target_syllable,prepad=10,postpad=10,shuffle=False,n=50, notbatch='notbatch'):
    notmat_lines_list = list(open(bird_directory+notbatch))
    notmat_list = [bird_directory+value[:value.index('\n')] for value in notmat_lines_list]
    if shuffle==True:
        random.shuffle(notmat_list)
    f=0
    syllable_directory = bird_directory+'/'+target_syllable+'/'
    if not os.path.exists(syllable_directory):
        os.mkdir(syllable_directory)
    for file in notmat_list:
        ndict = evfuncs.load_notmat(file)
        wav_file = file.strip('.not.mat')
        file_audio = AudioSegment.from_wav(wav_file)
        i=0
        for syl in ndict['labels']:
            if syl == target_syllable and spectrograms_created < n:
                onset=ndict['onsets'][i]
                offset=ndict['offsets'][i]
                syl_snippet = file_audio[onset-prepad:offset+postpad]
                ID = str(f)+'_'+str(i)
                snippet_filename = syllable_directory+'/'+ID+'.wav'
                syl_snippet.export(snippet_filename,format='wav')
                i+=1
        f+=1