# BF-NGRAMS
This package contains scripts for analyzing transitional probabilities and Shannon entropy using various orders of Markov models. Input sequences are strings of characters, where each character is read as a "word" (as per birdsong labelling conventions).

## Setup
You must have NLTK and numpy installed:
```pip install nltk```
```pip install numpy```

Next, download all the files here into a single folder, and create a subfolder alongside them called ```data```, where you put all input files, and another called ```output```, which you can leave empty.
 
## Input file format
Files should be .csv. The second column of each row contains a song (string of characters, no spaces). The first column is ignored. In my files, this has the name of the original audio file this song came from, e.g:
```gy54cy91_27918_748.2274.cbin.not.mat,iiiiiaiiibcdaibcdfgdfmdkiebcdfgdfmdkiiibcdfimg
gy54cy91_27918_117.382.cbin.not.mat,iiiiaiiaiibcdaebcdiiebcdfimgdfmdkifebcdebcdfim
```
The name of the file should begin with the bird ID - if not, just make sure it's at least 8 characters long, or there might be trouble.

## Usage
From a Python shell, doing
```index.get_probs(filepath, nrange) ```
gives you the transitional probabilities for the data in filepath, given Markov models specified in nrange. nrange is a list of two n values: [n1,n2]. The first is the minimum n-value you're interested in probabilities for, the second is one more than the maximum you're interested in. e.g. [2,4] gives you data for bigrams and trigrams; [2,3] gives you only bigram info. output format: a dictionary of all n-gram probabilities for each of the n-values contained in nrange. IMPORTANT: "2" is a first-order Markov model, "3" is a second-order one, and so on. Add one to the order of the MM to get the n you should input. This returns a dictionary over the n values in nrange, and also outputs a file labelled accordingly into the folder 

Doing
```ent.combined(filepath,nrange,backoff=1)```
takes an input corpus, and outputs entropy estimates for that corpus, given Markov models of the various orders specified in nrange. 

The algorithm runs as follows. The corpus is iteratively divided into a training set containing all but one song, and a test set which contains the held out song. For each iteration, the entropy of each syllable in the held out song is calculated by using probabilities calculated by the previous function, and the following formula for Shannon entropy:
https://wikimedia.org/api/rest_v1/media/math/render/svg/f96cf5194b9102f383a05c04c8994e7af8b161fb
At the end of each song, the entropy values for each syllable are averaged. The final output is an average of the song entropies for each iteration, which estimates the entropy of the song as a whole. Again, the result is a dictionary over the n values in nrange (even if there is only one). It outputs a file called ```entropy.csv```, and overwrites the old file each time you call the function, so make sure to keep a copy.

The algorithm automatically employs "backoff" to deal with data scarcity at higher orders of Markov model. This means that if it is unable to find an entropy estimate for the current syllable given the n syllables before it, it tries to find one for n-1, and so on down to 2. If the bigram which that syllable completes is a hapax legomenon in the corpus - that is, it occurs nowhere else, then an entropy value of ```not_found``` is stored. To turn backoff off, put ```backoff=0``` as the third argument. This results in many more blank entropy estimates, due to the frequency of hapax legomena at high-orders, and thus increases the size of the corpus needed to achieve reasonable entropy estimates. But only with backoff turned off are the entropy estimates truly reflective of strictly nth-order Markov models - with Backoff on, they reflect an opportunistic hybrid between lower-order and higher order models.

