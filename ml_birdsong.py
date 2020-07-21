import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import get_train
import numpy as np

def get_data(train = 0.5, test = 0.3, val = 0.2):
    x,y = get_train.get_feat_data()
    y = [value[0][-1] for value in y]
    y_num = [ord(value) for value in y]
    y_targets = list(set(y_num))
    targets_consecutive = [y_targets.index(value) for value in y_num]
    y = np.array(targets_consecutive)
    first_delim = round(len(x)/train)
    second_delim = -round(len(x)/val)
    x_train = x[:first_delim]
    y_train = y[:first_delim]
    x_test = x[first_delim:second_delim]
    y_test = y[first_delim:second_delim]
    x_val = x[second_delim:]
    y_val = y[second_delim:]
    return x_train,y_train,x_test,y_test,x_val,y_val