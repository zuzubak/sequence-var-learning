# generates ngrams file in ./output/ngrams.csv
import csv
from nltk import ngrams

all_songs = ''

with open('./data/r70ye50-songs.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    songs = []
    for row in csv_reader:
        print(row[1])
        songs.append(row[1])
        line_count += 1
    all_songs = ('/').join(songs)
    print('done')

print(all_songs)

n = 6
sixgrams = ngrams(all_songs.split(' '), n)

for grams in sixgrams:
    try: 
        print(grams)
    except:
        pass



    