import entropy
import csv
import random
import os
import re


def print_ent_estimates(fp, nrange, shuffle=False,birdID=None):
    '''
    Removes all but one song string (row) from the input file fp,
    Then adds the strings back in one at a time, re-estimating nth-order
    entropies using entropy.avg_ent() after each addition.
    Writes a csv file (./output/samplesize.csv) containing the entropy
    estimates for each sample size.
    '''
    mode = 'w'
    if birdID == None:
        out_fp = './output/samplesize.csv'
    else:
        out_fp = "./output/samplesize/%s.csv" %birdID
    with open(fp) as f:
        reader = csv.reader(f, delimiter="\n")
        lines_unformatted = list(reader)
        lines = []
        for line in lines_unformatted:
            lines.append(line[0])
    if shuffle:
        random.shuffle(lines)
    for i in range(len(lines)):
        print(str(i) + ' of ' + str(len(lines)))
        line = lines[i]
        with open(fp, mode) as output_file:
            writer = csv.writer(output_file)
            writer.writerow(line.split(","))
        ent = entropy.avg_ent(fp, nrange)
        out_row = [i + 1]
        for value in ent.values():
            out_row.append(value)
        if i==0 or i%10==9:
            with open(out_fp, mode) as output_file:
                writer = csv.writer(output_file)
                writer.writerow(out_row)
        mode = 'a'

def batch(directory='./data/BFs_logan/data', nrange=[2,7]):
    for filename in os.listdir(directory):
        birdID_csv = re.sub('fathers_and_sons_from_logan - ','',filename)
        birdID = re.sub('.csv','',birdID_csv)
        print(birdID)
        print_ent_estimates(directory+'/'+filename,nrange,birdID=birdID)

def asymptotes(directory='./output/samplesize'):
    for filename in os.listdir(directory):
        rows=list(open(directory+'/'+filename))

