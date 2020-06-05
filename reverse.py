from scipy.io import wavfile
import numpy as np
import math

def backwify(fp):
    rate, data = wavfile.read(fp)
    data_flipped=np.flip(data)
    return rate, data_flipped

def write_backwards(fp):
    rate, data_flipped  = backwify(fp)
    wavfile.write('./output/backwards.wav',rate,data_flipped)

def write_forwards_backwards(fp):
    rate, data_flipped  = backwify(fp)
    data = np.flip(data_flipped)
    data_forwards_backwards = []
    for value, ualue in zip(data, data_flipped):
        new_value_0 = value[0]+ualue[0]
        new_value_1 = value[1]+ualue[1]
        data_forwards_backwards.append([new_value_0,new_value_1])
    wavfile.write('./output/forwards_backwards.wav',rate,np.array(data_forwards_backwards))

def write_sine(fp):
    rate, data = wavfile.read(fp)
    out_data = []
    data = [value[0] for value in data]
    mid_data = max(data)-min(data)
    len_data = len(data)
    for i in range(len_data):
        try:
            j = len(data)*math.sin(2*i/len(data))
            #i_normalized = data[i]/max(data)*math.pi/2
            out_data.append(data[round(j)])
            print(str(i)+' of '+str(len(data)))
            if i%1000000==0:
                wavfile.write('./output/write_sin.wav',rate,np.array(out_data))
        except:
            wavfile.write('./output/write_sin.wav',rate,np.array(out_data))
            break
