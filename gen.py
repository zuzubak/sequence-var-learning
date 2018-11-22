import random
import nltk

probs={('a', 'e', 'c'): 1.0, ('i', 'i', 'a'): 0.10989010989010989, ('a', 'd', 'c'): 1.0, ('g', 'g', 'f'): 0.8928571428571429, ('b', 'a', 'i'): 0.2, ('d', 'e', 'c'): 0.75, ('f', 'f', 'f'): 0.9052287581699346, ('h', 'h', 'i'): 0.6, ('c', 'd', 'c'): 0.425, ('f', 'f', 'g'): 0.09477124183006536, ('g', 'h', 'h'): 1.0, ('d', 'e', 'a'): 0.1, ('c', 'c', 'd'): 1.0, ('a', 'b', 'a'): 1.0, ('a', 'a', 'i'): 0.3225806451612903, ('e', 'c', 'd'): 1.0, ('i', 'c', 'd'): 1.0, ('i', 'e', 'a'): 0.13333333333333333, ('h', 'h', 'h'): 0.4, ('i', 'i', 'h'): 0.06593406593406594, ('d', 'e', 'f'): 0.15, ('d', 'c', 'd'): 1.0, ('i', 'h', 'h'): 1.0, ('i', 'i', 'i'): 0.6373626373626373, ('d', 'a', 'a'): 1.0, ('e', 'f', 'f'): 1.0, ('h', 'i', 'i'): 1.0, ('i', 'e', 'i'): 0.8, ('a', 'i', 'i'): 1.0, ('c', 'd', 'e'): 0.5, ('e', 'i', 'i'): 1.0, ('g', 'g', 'h'): 0.10714285714285714, ('i', 'a', 'a'): 1.0, ('a', 'c', 'c'): 1.0, ('b', 'a', 'a'): 0.3, ('a', 'a', 'e'): 0.03225806451612903, ('i', 'e', 'c'): 0.06666666666666667, ('a', 'a', 'b'): 0.22580645161290322, ('g', 'f', 'f'): 1.0, ('b', 'a', 'c'): 0.1, ('a', 'a', 'c'):0.06451612903225806, ('f', 'g', 'g'): 0.9655172413793104, ('b', 'a', 'b'): 0.2, ('i', 'i', 'e'): 0.16483516483516483, ('f', 'g', 'f'): 0.034482758620689655, ('c', 'd', 'a'): 0.075, ('e', 'a', 'a'): 1.0, ('a', 'a', 'a'): 0.3548387096774194, ('i', 'i', 'c'): 0.01098901098901099, ('b', 'a', 'd'): 0.2}
'''def gen(txt):
    text=txt.split(' ')
    #text=nltk.corpus.gutenberg.words('austen-emma.txt')
    bigrams=nltk.bigrams(" ".join(text))
    print(list(bigrams))
    cfd=nltk.ConditionalFreqDist(bigrams)
    print(list(cfd))
    word=random.choice(" ".join(text))
    s1=[]
    for i in range(11):
        s1.append(choice(list())
    return s1'''

def get_trainTokens(genre):
    os.chdir(directory + 'train_books/'+str(genre))
    all_tokens = []
    print "tokenizing " + genre + " books...."
    for file in glob.glob("*.txt"):
        f = open(file)
        tokens = nltk.word_tokenize(f.read().decode("latin1"))
        all_tokens += tokens
        f.close()
    return all_tokens

def get_uniCounts(all_tokens):
    unigram_table = {}
    for token in all_tokens:
        if token in unigram_table:
            unigram_table[token] += 1
        else:
            unigram_table[token] = 1
    return unigram_table, len(all_tokens)

def get_biCounts(all_tokens):
    uniCounts, length = get_uniCounts(all_tokens)
    bigram_table = {}
    num_bigrams = 0
    for x in range(0, length - 1):
        if all_tokens[x] in bigram_table:
            if all_tokens[x + 1] in bigram_table[all_tokens[x]]:
                bigram_table[all_tokens[x]][all_tokens[x + 1]] += 1
            else:
                bigram_table[all_tokens[x]][all_tokens[x + 1]] = 1
                num_bigrams += 1
        else:
            bigram_table[all_tokens[x]] = {}
            bigram_table[all_tokens[x]][all_tokens[x + 1]] = 1
            num_bigrams += 1
    return bigram_table, num_bigrams

def get_biSentence(min,max,genre,sentence=''):
    print "computing bigrams and generating random sentence:"
    table=get_biTable(genre)
    length=len(sentence)
    if length==0:
        sentence=random_next(table['.'])
    sentence_tokens=nltk.word_tokenize(sentence)
    last_word=sentence_tokens[-1]
    for x in range(max):
        generating=True
        while (generating):
            if last_word in table:
                next=random_next(table[last_word])
            else:
                next=random.choice(table.keys())
            generating=False
            if (next=='.' and len<min):
                generating=True
        sentence=sentence+' '+next
        if next=='.':
            return sentence
        length+=1
        last_word=next
    return sentence+'.'

s2=get_biSentence(5,50,genre, 'I must')
            
            