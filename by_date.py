import index

def get_probs_by_date(filepath,ngram,date_range):
    order=len(ngram)
    odct={}
    for date in date_range:
        date=str(date)
        date_string=index.get_data_string(filepath,date=date)
        probs_dict=index.get_probs_from_string(date_string,[order,order+1])
        if tuple(ngram) in probs_dict[order].keys():
            odct[date]=probs_dict[order][tuple(ngram)]
        else:
            pass
    index.save_to_file(odct,filepath,order,name='by_date')
    return odct