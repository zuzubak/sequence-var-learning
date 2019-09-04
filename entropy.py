import math
import index
import csv
import shuffle

def calculate_bias(filepath,nrange):
    '''
    Create a bias term to add to entropy estimations of p_to_ent, using sample size and other
    characteristics of input strings. To be completed.
    '''
    pass
    

def p_to_ent(filepath,nrange):
    '''
    Calculates probability distributions for the songs in filepath for the nth order MMs included in nrange,
    then using each nth-order prob distr, calculates the entropy at each (n-1)gram.
    For hapax legomena, returns an H of 0.
    '''
    idct=index.get_probs(filepath,nrange)
    out_dict={}
    for n in idct.keys():
        ngram_dict=idct[n]
        ngram_count_list=[]
        for value in ngram_dict.values():
            ngram_count_list.append(value[1]) 
        total_ngram_count=sum(ngram_count_list)
        beginnings_dict={}
        for ngram in ngram_dict.keys():
            if ngram[:-1] not in beginnings_dict.keys(): 
                beginnings_dict[ngram[:-1]]=[[],[],[]]
        for ngram,prob_count in ngram_dict.items():
            beginnings_dict[ngram[:-1]][0].append(ngram)
            beginnings_dict[ngram[:-1]][1].append(prob_count[0])
            beginnings_dict[ngram[:-1]][2].append(prob_count[1])    
        entropy_dict={}
        for beginning in beginnings_dict.keys():
            probabilities_list=beginnings_dict[beginning][1]
            counts_list=beginnings_dict[beginning][2]
            ngrams_list=beginnings_dict[beginning][0]
            entropy_terms=[]
            i=0
            for probability in probabilities_list:
                unconditional_probability=counts_list[i]/total_ngram_count
                ngram=ngrams_list[i]
                entropy_terms.append(probability*math.log(probability,2))
                i+=1
            entropy_dict[beginning]= (-1*sum(entropy_terms),sum(counts_list))
        out_dict[n]=entropy_dict
    return (out_dict)
    
def avg_ent(filepath,nrange,shuffle_mode=False):
    '''
    For each n (Markov order) in the parameter nrange, averages entropy 
    across all n-grams, estimating the entropy rate of the songs in filepath.
    '''
    if shuffle_mode==True:
        shuffle.shuffle(filepath)
        filepath='./output/shuffle.csv'
    ndct=p_to_ent(filepath,nrange)
    #print(ndct)
    result={}
    for key,value in ndct.items():
        n=key
        ls=[]
        for jey,ualue in value.items():
            #if ualue[1]>1:
            for i in range(ualue[1]):
                ls.append(ualue[0])
        #if len(ls)>0:
            result[key]=sum(ls)/len(ls)
        '''else:
            result[key]='-'''
    with open("./output/entropy.csv", 'w') as output_file:
        writer = csv.writer(output_file)
        for key, value in result.items():
            row=[]
            row.append(key)
            row.append(value)
            writer.writerow(row)
    return result

def get_ngram_entropy(filepath,ngram):
    if type(ngram)==str:
        ngram=tuple(ngram)
    nrange=[2,len(ngram)+2]
    entropy_dict=p_to_ent(filepath,nrange)
    relevant_dict=entropy_dict[len(ngram)+1]
    if ngram in relevant_dict.keys():
        result=relevant_dict[ngram]
    else:
        result='ngram_not_found'
    return result

def get_ngram_counts(filepath,ngram):
    if type(ngram)==str:
        ngram=tuple(ngram)
    nrange=[2,len(ngram)+2]
    probs_counts_dict=index.get_probs(filepath,nrange)
    relevant_dict=probs_counts_dict[len(ngram)]
    for key in relevant_dict.keys():
        relevant_dict[key]=relevant_dict[key][1]
    if ngram in relevant_dict.keys():
        result=relevant_dict[ngram]
    else:
        result='ngram_not_found'
    return result

def batch(filepath,ngram_list,mode):
    out_list=[]
    if mode=='counts':
        for ngram in ngram_list:
            out_list.append(get_ngram_counts(filepath,ngram))
    if mode=='entropy':
        for ngram in ngram_list:
            out_list.append(get_ngram_entropy(filepath,ngram))
    return out_list
