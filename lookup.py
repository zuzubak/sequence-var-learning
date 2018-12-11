#lookup() takes a dictionary of dictionaries containing n-gram probabilities (one dictionary for each n), 
#and an string, as input.
#it returns and saves to './output/lookup.csv' the n-grams probabilites for each ngram in the string,
#based on the input dict.
#n is set by the highest n value present in the ngrams input dict.
#uses backoff iff lower n's are provided in the input dict (idct).
#input dict is the output of index.get_probs() (also in this folder).

import csv
def nglist(istr,n): #list the ngrams 
    result=[]
    counter = 0
    for i in range(0,len(istr)-n+1):
        ngram=[]
        for i in range(0,n):
            ngram.append(istr[counter+i])
        result.append(tuple(ngram))
        counter=counter+1
    return result
def save_to_file(data_list,n):
    with open("./output/lookup.csv", 'w') as output_file:
        writer = csv.writer(output_file)
        for item in data_list:
            ngram_list=item[0]
            info=item[1]
            row=[]
            concat=''
            for item in ngram_list:
                row.append(item)
                concat=concat+item
            row.append(concat)
            for item in info:
                row.append(item)
            writer.writerow(row)
def lookup(idct,istr):
    n=idct.keys()[-1]
    ngramlist=nglist(istr,n)
    result=[]
    for ngram in ngramlist:
        minilist=[]
        minilist.append(ngram)
        if ngram in idct[n]:
            minilist.append([idct[n][ngram][0],n])
        else:  #backoff, using lower-n entries in input dict. a record of which n is used for each char is kept in the third column of the output csv file.
            for m, dct in idct.items():
                mgram=ngram[-m:]
                o=m+1
                ogram=ngram[-o:]
                if mgram in idct[m] and ogram not in idct[o]:
                    minilist.append([idct[m][mgram][0],m])
            if len(minilist)==1:
                minilist.append('not_found')
        result.append(minilist)
    save_to_file(result,n)
    return result
    print(n)
    

