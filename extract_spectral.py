import os
import csv
import rows_to_columns as rtc
import statistics
import collections

def extract(
        directory = './data/BFs_logan/spectral_new',
        prefix = 'spectral_raw - '):
    data_dict = {}
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
        data_dict[bird_ID]={}
        with open(filepath) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            data = list(csv_reader)
            inventory = data[0][-1]
            data_reformatted=[]
            for row in data:
                syllable = inventory[int(row[0])-1]
                bird_ID_syllable = bird_ID+'_'+syllable
                if inventory in row:
                    row.remove(inventory)
                if '' in row:
                    row.remove('')
                row_data = [float(value) for value in row[1:6]]
                row_data.append(bird_ID_syllable)
                data_reformatted.append(row_data)
            data_dict[bird_ID]['inventory'] = inventory
            data_dict[bird_ID]['data'] = data_reformatted
    return data_dict


def syllable_medians(
            directory = './data/BFs_logan/spectral_new',
            prefix = 'spectral_raw - ',
            feats = ['MeanFreq',
                'SpecDense',
                'Duration',
                'LoudEnt',
                'SpecTempEnt',
                'Label']):
    out_dict = {}
    extracted_dict = extract(directory, prefix)
    for bird_ID, bird_data in extracted_dict.items():
        bird_medians_dict = {}
        inventory = bird_data['inventory']
        inventory_with_IDs = []
        for syllable in inventory:
            inventory_with_IDs.append(bird_ID + '_' + syllable)
        data = bird_data['data']
        for syllable in inventory_with_IDs:
            relevant_rows = []
            for row in data:
                if row[-1] == syllable:
                    relevant_rows.append(row)
            columns = rtc.rtc(relevant_rows).items()
            syl_dict = {}
            for i,column in columns:
                if i in range(0,len(feats)-1):
                    new_column = [float(item) for item in column]
                    syl_dict[feats[i]] = statistics.median(new_column)
            bird_medians_dict[syllable] = syl_dict
        ordered_bird_dict = dict(collections.OrderedDict(sorted(bird_medians_dict.items())))
        out_dict[bird_ID] = ordered_bird_dict
    return out_dict
'''
def reformat_medians():
    previous_result=syllable_medians()
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
'''

def reformat_PCA():
    previous_result=syllable_medians()
    with open("./output/spectral_MK_PCA.csv", 'w') as output_file:
        writer = csv.writer(output_file)
        for birdID,bird_dict in previous_result.items():
            for syllable, syl_dict in bird_dict.items():
                row=[]
                for feature in list(syl_dict.values()):
                    row.append(feature)
                row.append(syllable)
                writer.writerow(row)

def PCA_tokens(directory = './data/BFs_logan/spectral_new'):
    birds_dict = extract(directory=directory)
    with open('./output/PCA_tokens.csv', 'w') as output_file:
        writer = csv.writer(output_file)
        for value in birds_dict.values():
            for row in value['data']:
                writer.writerow(row)


            