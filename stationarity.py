import ent
import csv
import index

def get_data_string(filepath,m,mchunks):
    all_songs = ''
    with open(filepath) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        songs = []
        for row in csv_reader:
            song=row[1]
            start_index=int(len(song)/mchunks)*m
            end_index=int(len(song)/mchunks)*(m+1)
            songs.append(song[start_index:end_index])
            line_count += 1
        all_songs = ('/').join(songs)
        print(all_songs)
    return all_songs

def s(filepath,nrange,mchunks):
    result={}
    data_string=index.get_data_string(filepath)
    for n in range(nrange[0],nrange[1]):
        n_result={}
        for m in range(0,mchunks):
            n_result[m]=ent.combined_from_string(get_data_string(filepath,m,mchunks),nrange)
        result[n]=n_result
    return result