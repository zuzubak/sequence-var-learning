import csv

def get_list(filepath):
    my_list=[]
    with open(filepath) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
                mini_list=[]
                for item in row:
                        mini_list.append(item)
                my_list.append(mini_list)
                line_count += 1
    return my_list

def expand(filepath):
        ls=get_list(filepath)
        print(ls)
        result=[]
        for song_entry in ls:
                filename=song_entry[0]
                Xdbc_2=int(song_entry[1])
                Xdbc_1=int(song_entry[2])
                length=int(song_entry[3])
                empty=song_entry[4]
                #print(length)
                i=2
                song_list=['e']
                while i<=length:
                        if i==Xdbc_1 or i==Xdbc_2:
                                song_list.append('c')
                        else:
                                if song_list[-1]=='e':
                                        song_list.append('c')
                                else:
                                        if song_list[-1]=='c':
                                                song_list.append('e')
                        i+=1
                if empty=='n',song_list=song_list[:-1]
                result.append(song_list)
        with open("./output/expand.csv", "w") as output_file:
                writer = csv.writer(output_file)
                for item in result:
                        writer.writerow(item)
