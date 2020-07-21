def get_feat_data(
    filepath = './output/PCA_tokens.csv',
    features = [
        'MeanFreq',
        'SpecDense',
        'Duration',
        'LoudEnt',
        'SpecTempEnt'],
    mode = 'PCA',
    n_components=5):
    '''
    Code modified from https://towardsdatascience.com/pca-using-python-scikit-learn-e653f8989e60
    '''
    features_with_target = features.copy()
    features_with_target.append('target')
    import pandas as pd
    # load dataset into Pandas DataFrame
    df = pd.read_csv(filepath, names=features_with_target)
    from sklearn.preprocessing import StandardScaler
    # Separating out the features
    x = df.loc[:, features].values
    # Separating out the target
    y = df.loc[:, ['target']].values
    # Standardizing the features
    x = StandardScaler().fit_transform(x)

    return x,y