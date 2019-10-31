import csv

def get_raw_data(fp):
    raw_data=[]
    with open(fp) as csvfile:
        csvreader=csv.reader(csvfile,delimiter=',')
        for row in csvreader:
            for item in row:
                if item=='':
                    row=row.remove(item)
            raw_data.append(row)
    return raw_data