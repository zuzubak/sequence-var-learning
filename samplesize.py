import entropy
import csv
import random


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
