import csv

with open('./data/r70ye50-songs.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    songs = []
    for row in csv_reader:
        print(row[1])
        songs.append(row[1])
        line_count += 1
    print('done')