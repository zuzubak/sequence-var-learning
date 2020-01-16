import pickle
from varname import varname


def f_open(variable_name, mode):
        return open('./data/variables/'+variable_name+'.txt', mode)

def picklify(variable,variable_name):
    with f_open(variable_name,'wb') as fopen:
        pickle.dump(variable, fopen)

def depickle(variable_name):
    with f_open(variable_name,'rb') as fopen:
        return pickle.load(fopen)

    
    
