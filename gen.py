import random
import nltk


def get_trainTokens(genre):
    os.chdir(directory + 'train_books/' + str(genre))
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


def get_biSentence(min, max, genre, sentence=''):
    print "computing bigrams and generating random sentence:"
    table = get_biTable(genre)
    length = len(sentence)
    if length == 0:
        sentence = random_next(table['.'])
    sentence_tokens = nltk.word_tokenize(sentence)
    last_word = sentence_tokens[-1]
    for x in range(max):
        generating = True
        while (generating):
            if last_word in table:
                next = random_next(table[last_word])
            else:
                next = random.choice(table.keys())
            generating = False
            if (next == '.' and len < min):
                generating = True
        sentence = sentence + ' ' + next
        if next == '.':
            return sentence
        length += 1
        last_word = next
    return sentence + '.'


s2 = get_biSentence(5, 50, genre, 'I must')
