import pandas as pd
from sklearn import manifold

def apply_lens(df, lens='mds', n_dim=2):
    '''
    input: N x F dataframe of observations
    output: N x n_dim image of input data under lens function
    '''
    
    if lens != 'mds':
        raise 'error: only MDS lens is currently supported'
    if n_dim > 2 or n_dim < 1:
        raise 'error: image of data set must be dimension 1 or 2'
    

    df_lens = pd.DataFrame(manifold.MDS(n_components=n_dim).fit_transform(df), df.index)
    return df_lens
