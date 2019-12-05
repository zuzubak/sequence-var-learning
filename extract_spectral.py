import os
import csv
import rows_to_columns as rtc
import statistics
import collections

def extract(
        directory='./data/BFs_logan/spectral_new',
        prefix='spectral_raw - '):
    out_dict = {}
    data_dict = {}
    feats = ['Label',
            'MeanFreq',
            'SpecDense',
            'Duration',
            'LoudEnt',
            'SpecTempEnt',
            'meanLoud']
    mode = 'w'
    for filename in os.listdir(directory):
        filepath=directory+'/'+filename
        fn_listchar = list(filename[:-4])
        pf_listchar = list(prefix)
        for char in pf_listchar:
            fn_listchar.remove(char)
        bird_ID = ''
        for char in fn_listchar:
            bird_ID += char
        with open(filepath) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            data = list(csv_reader)
            inventory = data[0][-1]
            for row in data:
                row[0] = inventory[int(row[0])-1]
            data_dict[bird_ID] = data
        bird_dict = {}
        for syllable in inventory:
            relevant_rows = []
            for row in data:
                if row[0] == syllable:
                    relevant_rows.append(row)
            columns = rtc.rtc(relevant_rows).items()
            syl_dict = {}
            for i,column in columns:
                if i in [1,2,3,4,5,6]:
                    new_column = [float(item) for item in column]
                    syl_dict[feats[i]] = statistics.median(new_column)
            bird_dict[syllable] = syl_dict
        ordered_bird_dict = dict(collections.OrderedDict(sorted(bird_dict.items())))
        out_dict[bird_ID] = ordered_bird_dict
    print(out_dict)
    return out_dict

def reformat():
    previous_result=extract()
    with open("./output/spectral_MK.csv", 'w') as output_file:
        writer = csv.writer(output_file)
        for birdID,bird_dict in previous_result.items():
            row = []
            row.append(birdID)
            for syllable, syl_dict in bird_dict.items():
                row.append(syllable)
                for feature in syl_dict.values():
                    row.append(feature)
                row.append('')
            writer.writerow(row)


def reformat_PCA():
    previous_result=extract()
    with open("./output/spectral_MK_PCA.csv", 'w') as output_file:
        writer = csv.writer(output_file)
        for birdID,bird_dict in previous_result.items():
            for syllable, syl_dict in bird_dict.items():
                row=[]
                for feature in list(syl_dict.values())[:-1]:
                    row.append(feature)
                row.append(birdID+'_'+syllable)
                writer.writerow(row)