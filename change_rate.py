from pydub import AudioSegment
import pareto
from scipy.io import wavfile
import numpy as np
import wave
import struct

def change(wav_filepath,window_length,window_spacing,change):
    origina_rate = wave.open(wav_filepath).getframerate()
    rate = origina_rate
    snippets = pareto.moving_windows(wav_filepath,window_length,window_spacing)
    data = []
    for snippet in snippets:
        f = wave.open('./output/acceleration_snippet.wav','w')
        f.setnchannels(1)
        f.setsampwidth(2)
        rate*=change
        print(rate)
        f.setframerate(round(rate))
        f.writeframesraw(np.array(snippet))
        f.close()
        h = wave.open('./output/acceleration_snippet.wav','r')
        snippet_data = []
        while h.tell() < h.getnframes():
            decoded = struct.unpack("<h", h.readframes(1))
            snippet_data.append(decoded)
        h.close()
        try:
            g = wave.open('./output/acceleration_output.wav','r')
            data = []
            while g.tell() < g.getnframes():
                decoded = struct.unpack("<h", g.readframes(1))
                data.append(decoded)
            g.close()
        except:
            pass
        data+=snippet_data
        i = wave.open('./output/acceleration_output.wav','w')
        i.setnchannels(1)
        i.setsampwidth(2)
        i.setframerate(origina_rate)
        i.writeframesraw(np.array(data))
        i.close()

        





