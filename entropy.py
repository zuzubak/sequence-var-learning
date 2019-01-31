import math
import index
import csv

def p_to_ent(string,nrange):
    idct=index.get_probs_from_string(string,nrange)
    ndct={}
    for key,value in idct.items():
        ent_dct={}
        for jey,ualue in value.items():
            if jey[0:key-2] not in ent_dct.keys():
                ent_dct[jey]=[ualue[0]*math.log(ualue[0],2)]
            else:
                ent_dct[jey[0:key-2]].append(ualue[0]*math.log(ualue[0],2))
        summed_dct={}
        for iey,talue in ent_dct.items():
            summed_dct[iey]=(0-(sum(talue)),'')
        ndct[key]=summed_dct
    return ndct
    
def avg_ent(string,nrange):
    ndct=p_to_ent(string,nrange)
    result={}
    for key,value in ndct.items():
        ls=[]
        for jey,ualue in value.items():
            ls.append(ualue)
        result[key]=sum(ls)/len(ls)
    with open("./output/entropy.csv", 'w') as output_file:
        writer = csv.writer(output_file)
        for key, value in result.items():
            row=[]
            row.append(key)
            row.append(value)
            writer.writerow(row)
    return result
