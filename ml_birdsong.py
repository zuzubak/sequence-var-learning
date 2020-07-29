import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import get_train
import numpy as np

#Data goes here: x is a numpy array of feature vectors, y is a numpy array of labels.

def get_data():
    x,y = get_train.get_feat_data()
    y = [value[0] for value in y]
    x_new = []
    y_new = []
    for i in range(len(x)):
        if 'tutor_br34bl20' in y[i]:
            x_new.append(x[i])
            y_new.append(y[i][-1])
    x = np.array(x_new)
    y = np.array(y_new)
    return x,y

def divide_data(train = 0.5, test = 0.3, val = 0.2, birds = 'all'):
    x,y = get_data()
    y_num = [ord(value) for value in y]
    y_targets = list(set(y_num))
    targets_consecutive = [y_targets.index(value) for value in y_num]
    y = np.array(targets_consecutive)
    first_delim = round(len(x)*train)
    second_delim = -round(len(x)*val)
    print(first_delim)
    print(second_delim)
    x_train = x[:first_delim]
    y_train = y[:first_delim]
    x_test = x[first_delim:second_delim]
    y_test = y[first_delim:second_delim]
    x_val = x[second_delim:]
    y_val = y[second_delim:]
    return x_train,y_train,x_test,y_test,x_val,y_val

def fit_model(epochs=100): # modified from https://www.tensorflow.org/guide/keras/train_and_evaluate
    x_train,y_train,x_test,y_test,x_val,y_val = divide_data()
    inputs = keras.Input(shape=(len(x_train[0]),), name="syllables")
    x = layers.Dense(64, activation="relu", name="dense_1")(inputs)
    x = layers.Dense(64, activation="relu", name="dense_2")(x)
    outputs = layers.Dense(len(list(set(y_train))), activation="softmax", name="predictions")(x)

    model = keras.Model(inputs=inputs, outputs=outputs)

    model.compile(
        optimizer=keras.optimizers.RMSprop(),  # Optimizer
        # Loss function to minimize
        loss=keras.losses.SparseCategoricalCrossentropy(),
        # List of metrics to monitor
        metrics=[keras.metrics.SparseCategoricalAccuracy()],
    )

    history = model.fit(
    x_train,
    y_train,
    batch_size=64,
    epochs=epochs,
    # We pass some validation for
    # monitoring validation loss and metrics
    # at the end of each epoch
    validation_data=(x_val, y_val),
    )

    return history

fit_model()