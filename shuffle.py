import random
import csv

def shuffle(fp,sample_size=1):
    '''
    Given a song file, shuffles the syllables of each song around randomly and writes 
    the shuffled songs to a new file, './output.shuffle.csv'
    '''
    for i in range(sample_size):
        with open(fp) as f:
                reader = csv.reader(f, delimiter="\n")
                lines_unshuffled=list(reader)
                lines=[]
                for line in lines_unshuffled:
                    print(line)
                    line_list=list(line[0].split(',')[1])
                    random.shuffle(line_list)
                    shuffled_string=''.join(line_list)
                    lines.append(shuffled_string)
        mode='w'
        for line in lines:
            with open('./output/shuffle.csv', mode) as output_file:
                writer = csv.writer(output_file)
                writer.writerow(['-',line])
                mode='a'