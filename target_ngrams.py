import index
import entropy
import csv
import by_date
import spectral_feats

def get_ngram_spectral_feats(filepath,ngram,bird_ID):
    spect_dict=spectral_feats.make_dict(filepath)[bird_ID]
    means_dict={}
    feats=spect_dict[list(spect_dict.keys())[0]].keys()
    for feat in feats:
        means_dict[feat]=[]
    for char in ngram:
        if char in spect_dict.keys():
            for i in range(len(feats)):
                char_feat=list(feats)[i]
                means_dict[char_feat].append(float(spect_dict[char][char_feat]))
    for key,value in means_dict.items():
        print(key)
        print(value)
        if len(value)>0:
            means_dict[key]=sum(value)/len(value)
        else:
            means_dict[key]='no_data'
    return means_dict

def ngram_info(fp,n,target_syllable='all',min_count=5,probs=False):
    out_list=[]
    ngrams=index.get_probs(fp,[n,n+1])[n]
    target_ngrams=[]
    for ngram in ngrams.keys():
        if ngram[-1]==target_syllable or target_syllable=='all':
            ngram_string=''
            for char in ngram:
                ngram_string=ngram_string+char
            if ngram_string not in target_ngrams:
                target_ngrams.append(ngram_string)
    for ngram in target_ngrams:
        minilist=[ngram[:-1]]
        minilist.append(entropy.get_ngram_entropy(fp,ngram[:-1])[0])
        minilist.append(entropy.get_ngram_entropy(fp,ngram[:-1])[1])
        count=ngrams[tuple(ngram)][1]
        prob=ngrams[tuple(ngram)][0]
        if probs==True:
            minilist.append(prob)
        if count>=min_count:
            out_list.append(minilist)
    mode='w'
    for minilist in out_list:
        with open("./output/target_ngrams.csv", mode) as output_file:
                writer = csv.writer(output_file)
                writer.writerow(minilist)
        mode='a'
    return out_list

def info_and_feats(songs_fp,n,spectral_fp,bird_ID):
    info=ngram_info(songs_fp,n)
    out_list=[]
    for minilist in info:
        ngram=minilist[0]
        feats=get_ngram_spectral_feats(spectral_fp,ngram,bird_ID)
        for feat in feats.values():
            minilist.append(feat)
        out_list.append(minilist)
    mode='w'
    for minilist in out_list:
        with open("./output/ngram_info_and_feats.csv", mode) as output_file:
                writer = csv.writer(output_file)
                writer.writerow(minilist)
        mode='a'
    return out_list

'''
    if ent_fp=='none':
        ent_fp=fp
'''

def info_and_dates(baseline_fp,dates_fp,target_syllable,n,start_date,end_date):
    info_list=ngram_info(baseline_fp,n,target_syllable)
    out_list=[]
    for row in info_list:
        mini_out_list=row
        ngram=row[0]+target_syllable
        print(ngram)
        dates_and_probs_list=by_date.get_probs_by_date(dates_fp,ngram,start_date,end_date)
        for date in dates_and_probs_list:
            mini_out_list.append(date[1])
        out_list.append(mini_out_list)
    mode='w'
    for minilist in out_list:
        with open("./output/target_ngrams_with_dates.csv", mode) as output_file:
                writer = csv.writer(output_file)
                writer.writerow(minilist)
        mode='a'
    return out_list