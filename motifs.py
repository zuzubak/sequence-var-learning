import csv
import index
from collections import Counter
from nltk import ngrams
import math

#motifs =[['B','e','bcd'],['G','m','gd'],['K','m','dk']]
motifs = [['B', 'e', 'bcd'], ['G', 'm', 'gd'], ['K', 'm', 'dk']]
motif_list = []
for item in motifs:
    motif_list.append(item[0])


def data(filepath, mode=False):
    with open(filepath) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        data = list(csv_reader)
    songs = []
    if not mode:
        for item in data:
            songs.append(item[1])
    return songs


def get_motif_indices(filepath):
    songs = data(filepath)
    i = 0
    motifs_list = []
    for song in songs:
        for j in range(len(song)):
            m_list = [i]
            for motif in motifs:
                if song[j:j + len(motif[2])] == motif[2]:
                    m_list.append(motif[0])
                    m_list.append(j)
                    m_list.append(j + len(motif[2]))
                    motifs_list.append(m_list)
        i += 1
    return motifs_list


def motif_string(filepath, ignore_repeats=False):
    indices = get_motif_indices(filepath)
    string = ''
    song_number = 0
    for minilist in indices:
        if minilist[0] != song_number:
            string = string + '/'
            song_number = minilist[0]
        to_add = minilist[1]
        try:
            if ignore_repeats and minilist[1] == string[-1]:
                to_add = ''
        except BaseException:
            pass
        string = string + to_add
    return string


def filler_len(filepath):
    songs = data(filepath)
    motif_indices = get_motif_indices(filepath)
    result = []
    new_result = {}
    for motif1 in motif_list:
        for motif2 in motif_list:
            motif_list = [(motif1, motif2), []]
            for i in range(len(motif_indices) - 1):
                if motif_indices[i][1] == motif1:
                    if motif_indices[i + 1][1] == motif2:
                        if motif_indices[i][0] == motif_indices[i + 1][0]:
                            motif_list[1].append(
                                motif_indices[i + 1][2] - motif_indices[i][3])
            result.append(motif_list)
    for item in result:
        try:
            new_result[item[0]] = sum(item[1]) / len(item[1])
        except BaseException:
            new_result[item[0]] = 'n/a'
    return new_result


def save_to_file(data_list):
    with open("./output/motifs.csv", 'w') as output_file:
        writer = csv.writer(output_file)
        for item in data_list:
            writer.writerow(item)


def filler_len_individual(filepath):
    songs_string = motif_string(filepath)
    motif_indices = get_motif_indices(filepath)
    probs = index.get_probs_from_string(songs_string, [2, 3])[2]
    print(probs)
    result = []
    for i in range(len(motif_indices) - 1):
        if motif_indices[i][0] == motif_indices[i + 1][0]:
            minilist = [motif_indices[i][1], motif_indices[i + 1][1]]
            minilist.append(probs[tuple(minilist)][0])
            minilist.append(motif_indices[i + 1][2] - motif_indices[i][3])
            result.append(minilist)
    save_to_file(result)
    return result


def filler(filepath):  # returns a list of all motif bigrams tokens, sandwiching the material that occurs between them
    songs = data(filepath)
    motif_indices = get_motif_indices(filepath)
    result = []
    for item in motif_indices[:-1]:
        next_item = motif_indices[motif_indices.index(item) + 1]
        song_number = item[0]
        if next_item[0] == song_number:
            filler_start_ind = item[3]
            filler_end_ind = next_item[2]
            result.append([item[1], songs[song_number]
                           [filler_start_ind:filler_end_ind], next_item[1]])
    return result


# returns a dictionary for all motifs of which motifs precede and follow
# that motif most often.
def get_context(filepath, rare_transitions_only=False):
    filler_list = filler(filepath)
    fillers = {}
    for item in filler_list:
        if item[1] not in fillers.values():
            pre = {'B': 0, 'G': 0, 'K': 0}
            post = {'B': 0, 'G': 0, 'K': 0}
            for jtem in filler_list:
                go_ahead = True
                if rare_transitions_only:
                    common_transitions = [('B', 'G'), ('G', 'K'), ('K', 'B')]
                    for ktem in common_transitions:
                        if jtem[0] == ktem[0] and jtem[2] == ktem[1]:
                            go_ahead = False
                if jtem[1] == item[1] and go_ahead:
                    pre[jtem[0]] += 1
                    post[jtem[2]] += 1
            fillers[item[1]] = {'pre': pre, 'post': post}
    return fillers


# determines whether the material to the left or the right of a given
# motif is more correlated with that motif.
def bias(filepath, rare_transitions_only=False):
    fillers = get_context(filepath, rare_transitions_only)
    pre_sum_list = []
    for value in get_context(filepath, rare_transitions_only).values():
        for walue in value['pre'].values():
            pre_sum_list.append(walue)
    length = sum(pre_sum_list)
    pre_list = []
    post_list = []
    for filler in fillers.keys():
        max_pre = max(fillers[filler]['pre'].values())
        max_post = max(fillers[filler]['post'].values())
        pre_list.append(max_pre)
        post_list.append(max_post)
    return {'pre': sum(pre_list) / length, 'post': sum(post_list) / length}


def counts_to_p(idct):
    odct = {}
    for key, value in idct.items():
        denominator = sum(value.values())
        odct[key] = {}
        for jey, ualue in value.items():
            odct[key][jey] = ualue / denominator
    return odct


def p_to_ent(idct):
    idct = counts_to_p(idct)
    ent_dict = {}
    for key, value in idct.items():
        ent_dict[key] = 0
        entropy = 0
        for ualue in value.values():
            entropy += ualue * math.log(ualue, 2)
        entropy = -entropy
        ent_dict[key] = entropy
    return ent_dict


def ent(fp):
    filler_list = filler(fp)
    motif_bigrams = []
    filler_motif_bigrams = []
    for item in filler_list:
        motif_bigrams.append([item[0], item[2]])
        filler_motif_bigrams.append([item[1], item[2]])
    out_dict = {'motifs': {}, 'fillers': {}}
    i = 0
    for jtem in [motif_bigrams, filler_motif_bigrams]:
        motif_dict = {}
        if i == 0:
            key = 'motifs'
        if i == 1:
            key = 'fillers'
        for item in jtem:
            if item[0] not in motif_dict.keys():
                motif_dict[item[0]] = {}
            if item[1] not in motif_dict[item[0]].keys():
                motif_dict[item[0]][item[1]] = 1
            else:
                motif_dict[item[0]][item[1]] += 1
        out_dict[key] = motif_dict
        i += 1
    print(out_dict)
    result = {}
    for key, value in out_dict.items():
        result[key] = p_to_ent(value)
    return result
