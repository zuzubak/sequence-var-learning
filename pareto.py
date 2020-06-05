from pydub import AudioSegment
from scipy.io import wavfile
import umap
import numpy as np
from matplotlib import pyplot as plt
import os
import csv
from more_itertools import locate
import math
from scipy import stats

def moving_windows(wav_filepath,window_length,window_spacing): #times in seconds
    sampling_rate = wavfile.read(wav_filepath)[0]
    data = wavfile.read(wav_filepath)[1]
    if type(data[0]) is list:
        file_audio = [value[0] for value in data] #convert stereo to mono
    else:
        file_audio = data
    window_length*=sampling_rate
    window_spacing*=sampling_rate
    onset = 0
    offset = window_length
    snippets = []
    while offset <= len(file_audio):
        print(str(onset/sampling_rate)+' of '+str(len(file_audio)/sampling_rate)+' seconds')
        onset += window_spacing
        offset += window_spacing
        onset = round(onset)
        offset = round(offset)
        snippet = file_audio[onset:offset]
        snippets.append(snippet)
    return snippets
    
def umap_embedding(wav_filepath,window_length,window_spacing): #times in seconds
    w = moving_windows(wav_filepath,window_length,window_spacing)[:-1]
    w_matrix = np.array(w)
    reducer = umap.UMAP()
    embedding = reducer.fit_transform(w_matrix)
    #plt.scatter(embedding[:, 0], embedding[:, 1])
    #plt.show()
    return embedding

def batch_pareto(directory,window_length,window_spacing,output_filename='./output/batch_pareto.csv'):
    '''
    to_write = []
    for folder in os.listdir(directory):
        if os.path.isdir(directory+'/'+folder):
            for subfolder in os.listdir(directory+'/'+folder):
                if os.path.isdir(directory+'/'+folder+'/'+subfolder):
                    for wav_file in [file for file in os.listdir(directory+'/'+folder+'/'+subfolder) if file.endswith('.wav')]:
                        print(wav_file)
                        rate, audio_data = wavfile.read(directory+'/'+folder+'/'+subfolder+'/'+wav_file)
                        to_write+=(list(audio_data)[:60*rate])
    wavfile.write('./output/combined.wav',44100,np.array(to_write))
    '''
    embedding = umap_embedding('./output/combined.wav',window_length,window_spacing)
    with open(output_filename, 'w') as myfile:
        wr = csv.writer(myfile)
        for row in embedding:
            wr.writerow(row)
    return embedding

def ranges(directory,wl_list):
    out_dict = {}
    for wl in wl_list:
        out_dict[wl] = batch_pareto(directory, wl, wl, output_filename='./output/buckeye_umap_1stmin_'+str(wl)+'_'+str(wl)+'.csv')
    return out_dict

def bin_umap_values(csv_file,pixels=20):
    with open(csv_file,'r') as fopen:
        data = list(csv.reader(fopen))
    numeric_matrix = []
    for row in data:
        numeric_matrix.append([float(value) for value in row])
    numeric_matrix = np.array(numeric_matrix)
    x_min = min(numeric_matrix[:,0])
    x_max = max(numeric_matrix[:,0])
    x_interval = (x_max-x_min)/pixels
    y_min = min(numeric_matrix[:,1])
    y_max = max(numeric_matrix[:,1])
    y_interval = (y_max-y_min)/pixels
    #return ((x_min,x_max),(y_min,y_max))
    x_gridlines = [x_min]
    y_gridlines = [y_min]
    while x_gridlines[-1] < x_max:
        x_gridlines.append(x_gridlines[-1] + x_interval)
    while y_gridlines[-1] < y_max:
        y_gridlines.append(y_gridlines[-1] + y_interval)
    out_dict = {}
    for i in range(pixels):
        for j in range(pixels):
            out_dict[(x_gridlines[i],y_gridlines[j])] = sum(1 if x_gridlines[i]<row[0]<x_gridlines[i+1] and y_gridlines[j]<row[1]<y_gridlines[j+1] else 0 for row in numeric_matrix)
    return out_dict

def batch_bin(directory,pixels=20):
    out_list = []
    for csv_file in [file for file in os.listdir(directory) if file.endswith('.csv')]:
        print(csv_file)
        underscore_indices = list(locate(csv_file,lambda a: a=='_'))
        window_length = csv_file[underscore_indices[-2]+1:underscore_indices[-1]]
        mini_list = sorted(list(bin_umap_values(directory+'/'+csv_file,pixels=pixels).values())) + [window_length]
        mini_list.reverse()
        out_list.append(mini_list)
    with open('./output/batch_bin.csv', 'w') as myfile:
        wr = csv.writer(myfile) 
        for row in out_list:
            wr.writerow(row)

def curvature(fp = './output/batch_bin.csv'):
    reader = csv.reader(open(fp))
    data = list(reader)
    data_dict = {}
    for row in data:
        data_dict[row[0]] = row[1:]
    out_dict = {}
    for window_length,counts_list in data_dict.items():
        counts_list_no_zeros = [int(count) for count in counts_list if count is not '0']
        log_counts_list = [math.log(count) for count in counts_list_no_zeros]
        log_ranks_list = [math.log(rank) for rank in list(range(1,len(log_counts_list)+1))]
        #matrix = [log_ranks_list,log_counts_list]
        #print((window_length,matrix))
        #curvatures_list = list(np.gradient(matrix))[0][0]
        out_dict[window_length] = stats.pearsonr(log_ranks_list,log_counts_list)[0]
    with open('./output/batch_bin_curvatures.csv', 'w') as myfile:
        wr = csv.writer(myfile) 
        for key,value in out_dict.items():
            wr.writerow([key,value])
    
    

