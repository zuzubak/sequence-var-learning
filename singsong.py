import random
import csv
rand=random.random()
def gen(idct,starter_string,n):
    total = 0
    result=starter_string
    nm1dict={}
    current_prior=(result[1],result[2])
    for i in range(0,n):
        choices=[]
        for key,value in idct.items():
            keystr=''
            for item in key:
                keystr=keystr+item
            key_relevant=keystr[:-1]
            result_relevant=result[-len(key)+1:]
            if key_relevant==result_relevant:
                for x in range(int(value[0]*100)):
                    choices.append(keystr[-1])
        next_char=random.choice(choices)
        result=result+next_char
        #print('result',i,result)
    #return choices
    return result
    return n

def csv2dict(filepath):
    with open(filepath, mode='r') as infile:
        reader = csv.reader(infile)
        with open('csv2dict.csv', mode='w') as outfile:
            writer = csv.writer(outfile)
            result = {rows[0]:rows[1] for rows in reader}
            return result
            print result

def singsong(idct,starter_string,len_of_strings,num_of_songs):
    songs_list=[]
    #idct=csv2dict(filepath)
    print idct
    for i in range(num_of_songs):
        song=gen(idct,starter_string,len_of_strings)
        songs_list.append(song)
    with open("./output/singsong.csv", "w") as output_file:
        writer = csv.writer(output_file)
        for song in songs_list:
            writer.writerow(song)

  