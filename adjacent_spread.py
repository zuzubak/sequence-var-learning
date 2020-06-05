import spectral_pca as spca
import spread

def adjacent_spread(mode = 'backward'):
    pca_data = spca.get_pca()
    out_dct = {}
    for bird_syl in set(pca_data['target']):
        out_dct[bird_syl] = []
    for i,j in zip(range(0,len(pca_data)-1),range(1,len(pca_data))):
        print(str(j)+' of '+str(len(pca_data)))
        syl = list(pca_data.loc[j])[-1]
        if mode == 'backward':
            previous_coordinates = list(pca_data.loc[i])[:-1]
            out_dct[syl].append(previous_coordinates)
        if mode == 'forward':
            try:
                next_coordinates = list(pca_data.loc[i+1])[:-1]
                out_dct[syl].append(next_coordinates)
            except BaseException:
                pass
    for key,value in out_dct.items():
        out_dct[key] = spread.spread(value)
    return out_dct


