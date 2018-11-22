# generates ngrams file in ./output/ngrams.csv
import csv
import nltk
import sys
from nltk import ngrams
import itertools
from nltk.util import ngrams
from collections import Counter
from nltk import word_tokenize

def get_data_string(filepath):
    all_songs = ''

    with open(filepath) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        songs = []
        for row in csv_reader:
            songs.append(row[1])
            line_count += 1
        all_songs = ('/').join(songs)

    return all_songs

def token(x):
    return nltk.word_tokenize(x)
def nc(string, n):
	return Counter(ngrams(token(string),n))
def ncounts(string,n):
	return Counter(ngrams(token(" ".join(string)),n))

def get_ngrams(filepath, n):
    songs_string = get_data_string(filepath)
    return ncounts(songs_string, n)


#result = get_ngrams('./data/r70ye50-songs.csv', 5)
#print(result)
def save_to_file(data_dict,filepath,n):
    print(data_dict)
    with open("./output/probabilities.csv", "w") as output_file:
        writer = csv.writer(output_file)
        for key, value in data_dict.items():
            songs_string = get_data_string(filepath)
            writer.writerow([key, value])

def get_probs(filepath, n):
    nGrams = get_ngrams(filepath, n)
    nMinusOne = get_ngrams(filepath, n-1)
    result = {}
    for gram in nGrams:
        key = gram[:n-1]
        prior = nMinusOne[key]
        probability = float(nGrams[gram]) / float(prior)
        result[gram] = probability 
    save_to_file(result,filepath,n)
    return result 