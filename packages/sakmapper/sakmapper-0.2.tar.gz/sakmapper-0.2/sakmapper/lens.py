import pandas as pd
from sklearn import decomposition, manifold


def apply_lens(df, lens='pca', n_dim=2):
    '''
    input: N x F dataframe of observations
    output: N x n_dim image of input data under lens function
    '''
    if n_dim != 2:
        raise 'error: image of data set must be two-dimensional'

    if lens == 'pca':
        df_lens = pd.DataFrame(decomposition.PCA(n_components=n_dim).fit_transform(df), df.index)
    elif lens == 'mds':
        df_lens = pd.DataFrame(manifold.MDS(n_components=n_dim).fit_transform(df), df.index)
    elif lens == 'neighbor':
        df_lens = pd.DataFrame(manifold.SpectralEmbedding(n_components=n_dim).fit_transform(df), df.index)
    else:
        raise 'error: only PCA, MDS, neighborhood lenses are currently supported'
    
    return df_lens