import dist
from dist import avg_ratio

maxs=[1000, 1500, 2000, 2500, 3000, 3500]
mins=[500, 1000, 1500, 2000, 2500, 3000]
odct={}

def metadist(idct):
    for i in range(len(maxs)):
        value=dist.avg_ratio(idct,200,mins[i],maxs[i])
        print(str(mins[i])+'to 'str(maxs[i])+': '+str(value))
        odct[[mins[i],maxs[i]]]=value
    return odct
