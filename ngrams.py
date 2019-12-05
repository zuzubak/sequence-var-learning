import index
import os
import csv

def ngram_size(nrange=[1,12],directory='./data/BFs_logan/data',threshold=0):
    mode = 'w'
    for filename in os.listdir(directory):
        prob_distrib = index.get_probs(directory+'/'+filename,nrange)
        counts_vec = []
        for n in prob_distrib.keys():
            n_count = 0
            for value in prob_distrib[n].values():
                if value[1] >= threshold:
                    n_count += value[1]
            counts_vec.append(n_count)
        row = [filename]
        for value in counts_vec:
            row.append(value)
        with open("./output/ngrams.csv", mode) as output_file:
            writer = csv.writer(output_file)
            writer.writerow(row)
        mode = 'a'