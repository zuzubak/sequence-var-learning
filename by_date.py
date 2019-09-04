import index
import csv
import datetime
import repeats

def get_probs_by_date(filepath,ngram,start_date,end_date):
    order=len(ngram)
    out_list=[]
    date_list=[start_date]
    while end_date not in date_list:
        last_date=date_list[-1]
        year=int('20'+last_date[-2:])
        month=int(last_date[2:4])
        day=int(last_date[:2])
        one_day=datetime.timedelta(1)
        last_date=datetime.date(year,month,day)
        new_date=last_date+one_day
        new_date_string=new_date.strftime('%d%m%y')
        date_list.append(new_date_string)
    for date in date_list:
        date=str(date)
        date_string=index.get_data_string(filepath,date=date)
        probs_dict=index.get_probs_from_string(date_string,[order,order+1])
        minilist=[date]
        if tuple(ngram) in probs_dict[order].keys():
            for item in probs_dict[order][tuple(ngram)]:
                minilist.append(item)
        else:
            minilist.append(0)
            minilist.append(0)
        out_list.append(minilist)
    with open('./output/by_date.csv','w') as f:
        for item in out_list:
            f.write(str(item[0])+','+str(item[1])+','+str(item[2])+"\n")
    return out_list

def get_reps_by_date(filepath,syllable,start_date,end_date):
    out_list=[]
    date_list=[start_date]
    while end_date not in date_list:
        last_date=date_list[-1]
        year=int('20'+last_date[-2:])
        month=int(last_date[2:4])
        day=int(last_date[:2])
        one_day=datetime.timedelta(1)
        last_date=datetime.date(year,month,day)
        new_date=last_date+one_day
        new_date_string=new_date.strftime('%d%m%y')
        date_list.append(new_date_string)
    for date in date_list:
        date=str(date)
        date_string=index.get_data_string(filepath,date=date)
        repeats_dict=repeats.repeats(date_string,syllable)
        minilist=[date]
        for value in repeats_dict.values():
            minilist.append(value)
        out_list.append(minilist)
    mode='w'
    for row in out_list:
        with open('./output/repeats_by_date.csv',mode) as output_file:
                writer = csv.writer(output_file)
                writer.writerow(row)
        mode='a'
    return out_list