import index

def f(filepath1,filepath2,nrange,min_dif=0.1,min_count=10):
    dict1=index.get_probs(filepath1,nrange)
    dict2=index.get_probs(filepath2,nrange)
    result={}
    for n in range(nrange[0],nrange[1]):
        difdict={}
        ndict1=dict1[n]
        ndict2=dict2[n]
        for ngram in ndict1.keys():
            if ngram in ndict2.keys():
                prob_dif=ndict1[ngram][0]-ndict2[ngram][0]
                count=max([ndict1[ngram][1],ndict2[ngram][1]])
                if abs(prob_dif)>=min_dif and count>=min_count:
                    difdict[ngram]=prob_dif
        result[n]=difdict
    return result

