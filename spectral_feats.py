import os
import csv

def make_dict(filepath):
        with open(filepath) as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=',')
                line_count = 0
                out_dict={}
                for row in csv_reader:
                        minidict={}
                        i=1
                        while i<=len(row)-1:
                                syllable=row[i]
                                syllable_dict={}
                                syllable_dict['MeanFreq']=row[i+1]
                                syllable_dict['SpecDense']=row[i+2]
                                syllable_dict['Duration']=row[i+3]
                                syllable_dict['LoudEnt']=row[i+4]
                                syllable_dict['SpecTempEnt']=row[i+5]
                                syllable_dict['MeanLoud']=row[i+6]
                                minidict[syllable]=syllable_dict
                                i+=8
                        out_dict[row[0]]=minidict
                        line_count += 1
        return out_dict