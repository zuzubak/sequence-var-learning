# 1,33.38336473,87.71296531,32.53968254,97.15626937,78.25050227,78813.66224,iabcwxyzqhesf

import os


def with_context(directory):
    for file in os.listdir(directory):
        i=0
        for line in list(open(file)):
            if i==0:
                