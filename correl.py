import scipy


def correl(x, y):
    return scipy.stats.pearsonr(x, y)
