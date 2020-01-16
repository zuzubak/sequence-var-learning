import numpy
from scipy.spatial import distance


def spread(matrix):
    matrix = [tuple(point) for point in matrix]
    centroid = (sum([point[0] for point in matrix])/len(matrix), 
        sum([point[0] for point in matrix])/len(matrix))
    spread = sum([distance.euclidean(centroid,point) for point in matrix])/len(matrix)
    return spread