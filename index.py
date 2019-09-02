# generates ngrams file in ./output/ngrams.csv
backoff=0

import csv
import nltk
import sys
from nltk import ngrams
import itertools
from nltk.util import ngrams
from collections import Counter
from nltk import word_tokenize

def get_probs_from_csv(filepath):
    all_probs=''
    with open(filepath) as csv_file:
        csv_reader=csv.reader(csv_file,delimiter=',')
        probs=list(csv_reader)
<<<<<<< HEAD

    return probs

def get_data_list(filepath,case_sensitive=False):
    with open(filepath) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        songs = []
        for row in csv_reader:
            if case_sensitive==False:
                songs.append(row[1].lower())
            else:
                songs.append(row[1])
            line_count += 1
    return songs

def get_data_string(filepath,date='all',case_sensitive=False):
    all_songs = ''
    with open(filepath) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        songs = []
        if date=='all':
            for row in csv_reader:
                if case_sensitive==False:
                    songs.append(row[1].lower().replace('0',''))
                else:
                    songs.append(row[1])
                line_count += 1
        else:
            for row in csv_reader:
                if date in row[0]:
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

def findlast(haystack, needle):
    parts= haystack.split(needle)
    return parts[-1]

def save_to_file(data_dict,filepath,n,name='probabilities'):
    with open("./output/probabilities.csv",'w') as output_file:
        writer = csv.writer(output_file)
        for key, value in data_dict.items():
            songs_string = get_data_string(filepath)
            row=[]
            concat=''
            for item in key:
                row.append(item)
                concat=concat+item
            row.append(concat)
            for item in value:
                row.append(item)
            writer.writerow(row)

def get_probs(filepath, nrange):
    metaresult={}
    nlist=[]
    for i in range(nrange[0],nrange[1]):
        nlist.append(i)
<<<<<<< HEAD
    for n in nlist:
        nGrams = get_ngrams(filepath, n)
        result_with_slashes = {}
        if n==1:
            prior=sum(nGrams.values())
            for gram in nGrams:
                key = gram[0:n-1]
                probability = float(nGrams[gram]) / float(prior)
                result_with_slashes[gram] = (probability,nGrams[gram])
        else:
            nMinusOne = get_ngrams(filepath, n-1)
            for gram in nGrams:
                key = gram[0:n-1]
                prior = nMinusOne[key]
                probability = float(nGrams[gram]) / float(prior)
                result_with_slashes[gram] = (probability,nGrams[gram])
        result={}
        for key,value in result_with_slashes.items():
            if '/' not in key:
                result[key]=value
        save_to_file(result,filepath,n)
        metaresult[n]=result
    return metaresult

def get_probs_from_string(string, nrange):
=======

    return probs


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

def save_to_file(data_dict,filepath,n):
    with open("./output/%sprobabilities-%s.csv" %(filepath[7:-4],n), 'w') as output_file:
        writer = csv.writer(output_file)
        for key, value in data_dict.items():
            songs_string = get_data_string(filepath)
            row=[]
            concat=''
            for item in key:
                row.append(item)
                concat=concat+item
            row.append(concat)
            for item in value:
                row.append(item)
            writer.writerow(row)

def get_probs(filepath, nrange):
>>>>>>> test
    metaresult={}
    nlist=[]
    for i in range(nrange[0],nrange[1]):
        nlist.append(i)
<<<<<<< HEAD
    for n in nlist:
        nGrams = ncounts(string, n)
        nMinusOne = ncounts(string, n-1)
=======
    print(nlist)
=======
>>>>>>> test
    for n in nlist:
        nGrams = get_ngrams(filepath, n)
        nMinusOne = get_ngrams(filepath, n-1)
>>>>>>> test
        result_with_slashes = {}
        for gram in nGrams:
            key = gram[0:n-1]
            prior = nMinusOne[key]
            probability = float(nGrams[gram]) / float(prior)
            result_with_slashes[gram] = (probability,nGrams[gram])
        result={}
        for key,value in result_with_slashes.items():
            if '/' not in key:
                result[key]=value
<<<<<<< HEAD
=======
        save_to_file(result,filepath,n)
>>>>>>> test
        metaresult[n]=result
    return metaresult

def get_probs_from_string(string, nrange):
    metaresult={}
    nlist=[]
    for i in range(nrange[0],nrange[1]):
        nlist.append(i)
    for n in nlist:
        nGrams = ncounts(string, n)
        nMinusOne = ncounts(string, n-1)
        result_with_slashes = {}
        for gram in nGrams:
            key = gram[0:n-1]
            prior = nMinusOne[key]
            probability = float(nGrams[gram]) / float(prior)
            result_with_slashes[gram] = (probability,nGrams[gram])
        result={}
        for key,value in result_with_slashes.items():
            if '/' not in key:
                result[key]=value
        metaresult[n]=result
    return metaresult

    '''test_ngrams=n_grams(test_string,n)
    test_result={}
    for gram in test_ngrams:
        if gram in result:
            test_result[gram]=result[gram]
        else:
            test_result[gram]='not_found'''
    return result