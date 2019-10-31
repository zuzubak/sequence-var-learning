def get_pca(filepath='./data/pca_without_amplitude.csv',features=['MeanFreq', 'SpecDense', 'Duration', 'LoudEnt', 'SpecTempEnt']):
    '''
    Code modified from https://towardsdatascience.com/pca-using-python-scikit-learn-e653f8989e60
    '''
    features_with_target=features.copy()
    features_with_target.append('target')
    print(features)
    print(features_with_target)
    import pandas as pd
    # load dataset into Pandas DataFrame
    df = pd.read_csv(filepath, names = features_with_target)
    from sklearn.preprocessing import StandardScaler
    # Separating out the features
    x = df.loc[:, features].values
    # Separating out the target
    y = df.loc[:,['target']].values
    # Standardizing the features
    x = StandardScaler().fit_transform(x)

    from sklearn.decomposition import PCA
    pca = PCA(n_components=5)
    principalComponents = pca.fit_transform(x)
    principalDf = pd.DataFrame(data = principalComponents
                , columns = ['principal component 1', 'principal component 2', 'principal component 3','principal component 4','principal component 5'])

    finalDf = pd.concat([principalDf, df[['target']]], axis = 1)
    return finalDf

def pca_plot(filepath,targets,features=['MeanFreq', 'SpecDense', 'Duration', 'LoudEnt', 'SpecTempEnt',]):
    import matplotlib.pyplot as plt
    finalDf=get_pca(filepath,targets,features)
    fig = plt.figure(figsize = (8,8))
    ax = fig.add_subplot(1,1,1) 
    ax.set_xlabel('Principal Component 1', fontsize = 15)
    ax.set_ylabel('Principal Component 2', fontsize = 15)
    ax.set_title('2 component PCA', fontsize = 20)
    all_colours = ['r', 'g', 'b','y','c','m','k']
    colours=all_colours[:len(targets)]
    for target, colour in zip(targets,colours):
        indicesToKeep = finalDf['target'] == target
        ax.scatter(finalDf.loc[indicesToKeep, 'principal component 1']
                , finalDf.loc[indicesToKeep, 'principal component 2']
                , c = colour
                , s = 50)
    ax.legend(targets)
    ax.grid()
    plt.show()

def get_pca_matrix():
    pca_result=get_pca().values.tolist()
    out_dict={}
    for row in pca_result:
        print(row[:-2])
        birdID_syllable=row[-1]
        row.remove(row[-1])
        birdID=birdID_syllable[:-2]
        syllable=birdID_syllable[-1]
        if birdID not in out_dict.keys():
            out_dict[birdID]={}
        out_dict[birdID][syllable]=row
    return out_dict