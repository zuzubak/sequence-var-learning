import numpy
import os
import string
import index
import entropy

def get_previous_ent(syllable,n,ent_dict,probs_dict):
    '''
    ent_dict
    '''
    n_ent_dict=ent_dict[n]
    n_probs_dict=probs_dict[n]
    relevant_dict={}
    for ngram in n_probs_dict:
        if ngram[-1]==syllable:
            prefix=ngram[:-1]
            relevant_dict[prefix]=n_ent_dict[prefix]
    entropy_values=[]
    counts=[]
    for value in relevant_dict.values():
        entropy_values.append(value[0])
        counts.append(value[1])
    weighted_average=numpy.average(entropy_values,weights=counts)
    return weighted_average

def batch_pe(directory='./data/BFs_logan/data',n=2,prefix='fathers_and_sons_from_logan - '):
    result={}
    for filename in os.listdir(directory):
        fp=directory+'/'+filename
        fn_listchar=list(filename[:-4])
        pf_listchar=list(prefix)
        ent_dict=entropy.p_to_ent(fp,[2,n+1])
        probs_dict=index.get_probs(fp,[2,n+1])
        for char in pf_listchar:
            fn_listchar.remove(char)
        bird_ID=''
        for char in fn_listchar:
            bird_ID+=char
        result[bird_ID]={}
        for syllable in string.ascii_lowercase:
            try:
                print(get_previous_ent(syllable,n,ent_dict,probs_dict))
                result[bird_ID][syllable]=get_previous_ent(syllable,n,ent_dict,probs_dict)
            except:
                pass
    return result