import numpy
from scipy.spatial import distance
import random


def spread(matrix):
    matrix = [tuple(point) for point in matrix]
    centroid = []
    for i in range(len(matrix[0])):
        centroid.append(sum([point[i] for point in matrix])/len(matrix))
    centroid = tuple(centroid)
    spread = sum([distance.euclidean(centroid,point) for point in matrix])/len(matrix)
    return spread

def sim(matrix1, matrix2, iterations = 20):
    distances = []
    for i in range(iterations):
        random.shuffle(matrix1)
        random.shuffle(matrix2)
        for j in range(min([len(matrix1),len(matrix2)])):
            euclidean_distance = distance.euclidean(matrix1[j],matrix2[j])
            distances.append(euclidean_distance)
    average_distance = sum(distances)/len(distances)
    return average_distance
