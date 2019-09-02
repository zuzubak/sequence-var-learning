import entropy
import csv

def print_ent_estimates(fp,nrange):
    mode='w'
    with open(fp) as f:
        reader = csv.reader(f, delimiter="\n")
        lines_unformatted=list(reader)
        lines=[]
        for line in lines_unformatted:
            lines.append(line[0])
    for i in range(len(lines)):
        line=lines[i]
        with open(fp, mode) as output_file:
            writer = csv.writer(output_file)
            writer.writerow(line.split(","))
        ent=entropy.avg_ent(fp,nrange)
        out_row=[i+1]
        for value in ent.values():
            out_row.append(value)
        with open('./output/samplesize.csv', mode) as output_file:
            writer = csv.writer(output_file)
            writer.writerow(out_row)
        mode='a'