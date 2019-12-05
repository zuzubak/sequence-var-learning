import entropy
import csv
import random
import os


def print_ent_estimates(fp, nrange, shuffle=False):
    '''
    Removes all but one song string (row) from the input file fp,
    Then adds the strings back in one at a time, re-estimating nth-order
    entropies using entropy.avg_ent() after each addition.
    Writes a csv file (./output/samplesize.csv) containing the entropy
    estimates for each sample size.
    '''
    mode = 'w'
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
        with open('./output/samplesize.csv', mode) as output_file:
            writer = csv.writer(output_file)
            writer.writerow(out_row)
        mode = 'a'

def info_graphs(directory='./data/BFs_logan/data', nrange=[2,7], shuffle_mode=False, count_lst=[0,5,10], backwards=False):
    LOL = []
    mode = 'w'
    for filename in os.listdir(directory):
        info_profile = entropy.avg_ent(
            directory + '/' + filename, nrange, shuffle_mode, min_count, backwards = backwards)
        row = [filename]
        for value in info_profile.values():
            row.append(value)
        with open("./output/batchent.csv", mode) as output_file:
            writer = csv.writer(output_file)
            writer.writerow(row)
        mode = 'a'