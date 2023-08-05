from math import sqrt, cos, sin, pi
import numpy as np
import pandas as pd
from scipy.spatial.distance import pdist, squareform
import networkx as nx
from sklearn import cluster

def davies_bouldin(dist_mu, sigma):
    DB = 0
    K = len(sigma)
    for i in range(K):
        D_i = 0
        for j in range(K):
            if j == i:
                continue
            R_ij = (sigma[i] + sigma[j]) / dist_mu[i,j]
            if R_ij > D_i:
                D_i = R_ij
        DB += D_i
    return DB / K


def optimal_kmeans_clustering(df, points_highlighted):
    clustering = {}
    db_index = []
    X = df.ix[points_highlighted,:]
    for k in range(1, 6):
        kmeans = cluster.KMeans(n_clusters=k).fit(X)
        clustering[k] = pd.DataFrame(kmeans.predict(X), index=points_highlighted)
        dist_mu = squareform(pdist(kmeans.cluster_centers_))
        sigma = []
        for i in range(k):
            points_in_cluster = clustering[k][clustering[k][0] == i].index
            sigma.append(sqrt(X.ix[points_in_cluster,:].var(axis=0).sum()))
        db_index.append(davies_bouldin(dist_mu, np.array(sigma)))
    db_index = np.array(db_index[1:])
    k_optimal = np.argmin(db_index) + 2
    return [list(clustering[k_optimal][clustering[k_optimal][0] == i].index) for i in range(k_optimal)]


def mapper_graph(lens_data, resolution=10, gain=1, min_patch_occupancy=100, cover='rectangle'):
    '''
    input: N x n_dim image of of raw data under lens function, as a dataframe
    output: (undirected graph, list of node contents) 
    '''
    
    if cover != 'rectangle':
        raise 'error: only rectangular set covers are supported'

    cols = lens_data.columns
    xmin, xmax = lens_data[cols[0]].min(), lens_data[cols[0]].max()
    ymin, ymax = lens_data[cols[1]].min(), lens_data[cols[1]].max()
    width_x = (xmax - xmin) / resolution
    spill_over_x = gain * width_x
    width_y = (ymax - ymin) / resolution
    spill_over_y = gain * width_y

    lower_bound_x = np.arange(xmin, xmax, width_x) - spill_over_x
    upper_bound_x = np.arange(xmin, xmax, width_x) + width_x + spill_over_x
    lower_bound_y = np.arange(ymin, ymax, width_y) - spill_over_y
    upper_bound_y = np.arange(ymin, ymax, width_y) + width_y + spill_over_y

    patches = {}
    counter = 0
    for i in range(resolution):
        for j in range(resolution):
            points_highlighted = list(lens_data[(lens_data[cols[0]] > lower_bound_x[i]) &
                                                (lens_data[cols[0]] < upper_bound_x[i]) &
                                                (lens_data[cols[1]] > lower_bound_y[j]) &
                                                (lens_data[cols[1]] < upper_bound_y[j])
                                               ].index)
            if len(points_highlighted) > min_patch_occupancy:
                key = ((round(lower_bound_x[i],2), round(upper_bound_x[i],2)),
                       (round(lower_bound_y[j],2), round(upper_bound_y[j],2)))
                patches[key] = optimal_kmeans_clustering(lens_data, points_highlighted)
                counter += 1
    print 'total of {} patches required clustering'.format(counter)

    all_clusters = []
    for key in patches:
        all_clusters += patches[key]
    num_nodes = len(all_clusters)
    print 'this implies {} nodes in the mapper graph'.format(num_nodes)
    A = np.zeros((num_nodes, num_nodes))
    for i in range(num_nodes):
        for j in range(i):
            overlap = set(all_clusters[i]).intersection(set(all_clusters[j]))
            if len(overlap) > 0:
                A[i,j] = 1
                A[j,i] = 1
    
    G = nx.from_numpy_matrix(A)
    return G, all_clusters
