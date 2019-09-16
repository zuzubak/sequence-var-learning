import index

def repeats(fp_or_songs_str,syllable,max_count=5):
    '''Given either a songstrings file, or a list of song strings, and a specific syllable, 
    returns a dictionary of how many instances there are of the syllable being repeated n times, 
    from n=1 to n=max_count.
    '''
    count=0
    counts_dict={}
    for i in range(1,max_count+1):
        counts_dict[str(i)]=0
    try:
        songs_string=index.get_data_string(fp_or_songs_str)
    except:
        songs_string=fp_or_songs_str
    for char in songs_string:
        if char==syllable:
            count+=1
        else:
            if count>0:
                counts_dict[str(count)]+=1
            count=0
    return counts_dict