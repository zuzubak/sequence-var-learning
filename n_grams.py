from collections import defaultdict

def n_grams(string, n=1):
    """Returns an iterator over the n-grams given a list of tokens"""
    tokens=string
    shiftToken = lambda i: (el for j,el in enumerate(tokens) if j>=i)
    shiftedTokens = (shiftToken(i) for i in range(n))
    tupleNGrams = zip(*shiftedTokens)
    def display(tupleNGrams):
         s1 = []
         x=0
         for i in range(len(tupleNGrams)): # This is just to tell you how to create a list.
             s1.append(i+x)
             x=x+1
         return s1
    for ng,c in tupleNgrams:
        
    return dict(list(ngram_list)) # if join in generator : (" ".join(i) for i in tupleNGrams)