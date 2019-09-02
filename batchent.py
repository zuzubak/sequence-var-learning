import entropy
import os
import csv
import target_ngrams

def make_info_graphs(directory,nrange,shuffle_mode=False):
    LOL=[]
    mode='w'
    for filename in os.listdir(directory):
        print(filename)
        info_profile=entropy.avg_ent(directory+'/'+filename,nrange,shuffle_mode)
        print(info_profile)
        row=[filename]
        for value in info_profile.values():
            row.append(value)
        print(row)
        with open("./output/batchent.csv", mode) as output_file:
            writer = csv.writer(output_file)
            writer.writerow(row)
        mode='a'

def batch_syl_info_and_feats(directory,n,spectral_fp,prefix='fathers_and_sons_from_logan - '):
    LOL=[]
    mode='w'
    for filename in os.listdir(directory):
        fn_listchar=list(filename[:-4])
        pf_listchar=list(prefix)
        for char in pf_listchar:
            fn_listchar.remove(char)
        bird_ID=''
        for char in fn_listchar:
            bird_ID+=char
        tn_result=target_ngrams.info_and_feats(directory+'/'+filename,n,spectral_fp,bird_ID)
        for row in tn_result:
            row.insert(0,bird_ID)
            with open("./output/batch_syl_info_and_feats.csv", mode) as output_file:
                writer = csv.writer(output_file)
                writer.writerow(row)
            mode='a'
        for item in tn_result:
            if item not in LOL:
                LOL.append(item)
    return LOL

def nest_comparison(bird_IDs,directory,n,spectral_fp,index,prefix='fathers_and_sons_from_logan - ',previous_result='None',nest_name=''): #have to get rid of no_data rows, before using this for spectral analysis
    if type(previous_result) == list:
        pass
    else:
        previous_result=batch_syl_info_and_feats(directory,n,spectral_fp,prefix)
    bird_syls=[]
    for row in previous_result:
        bird_syls.append(row[:2])
    common_syllables=[]
    bird1=bird_IDs[0]
    bird1_syllables=[]
    for syl in bird_syls:
        print(syl)
        if syl[0]==bird1 and syl not in bird1_syllables:
            bird1_syllables.append(syl[1])
    print(bird1_syllables)
    current_list=bird1_syllables
    for bird in bird_IDs[1:]:
        current_bird_syllables=[]
        for syl in bird_syls:
            if syl[0]==bird and syl not in current_bird_syllables:
                current_bird_syllables.append(syl[1])
        current_list=list(set(current_list).intersection(current_bird_syllables))
    print(current_list)
    current_list.sort()
    header=bird_IDs
    header.insert(0,'Syllable')
    data=[header]
    for syllable in current_list:
        minilist=[syllable]
        birds_seen=[]
        for row in previous_result:
            if row[0] in bird_IDs and row[1]==syllable and row[0] not in birds_seen:
                minilist.append(row[index])
                birds_seen.append(row[0])
        data.append(minilist)
    mode='w'
    print(data)
    for row in data:
        with open("./nest_comparison/%s_nest_comparison.csv" % nest_name, mode) as output_file:
            writer = csv.writer(output_file)
            writer.writerow(row)
        mode='a'
    return data
