import statsmodels.formula.api as smf

def lmm(variables,data,groups):
    md = smf.mixedlm(variables,data,groups=groups)
    mdf = md.fit()
    return mdf.summary()