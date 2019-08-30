# Runs dist.avg_ratio iteratively over a range of maximum and minimum journey distances, specified in 'maxs' and 'mins'

import dist
from dist import avg_ratio

maxs=[1000, 1500, 2000, 2500, 3000, 3500, 4000]
mins=[500, 1000, 1500, 2000, 2500, 3000, 3500]
odct={}

def metadist(polygon,n_observations):
    for i in range(len(maxs)):
        value=dist.avg_ratio(polygon,n_observations,mins[i],maxs[i])
        print(str(mins[i])+'to '+str(maxs[i])+': '+str(value))
        odct[(mins[i],maxs[i])]=value
    return odct
