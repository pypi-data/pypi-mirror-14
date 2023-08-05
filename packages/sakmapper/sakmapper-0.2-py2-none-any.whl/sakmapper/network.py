from math import sqrt, cos, sin, pi
import numpy as np
import pandas as pd
from scipy.spatial.distance import pdist, squareform
import networkx as nx
from sklearn import cluster
from lens import apply_lens


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


def covering_patches(lens_data, resolution=10, gain=0.5, equalize=True):
    cols = lens_data.columns
    xmin, xmax = lens_data[cols[0]].min(), lens_data[cols[0]].max()
    ymin, ymax = lens_data[cols[1]].min(), lens_data[cols[1]].max()
    patch_dict = {}
    
    if equalize == True:
        perc_step = 100.0 / resolution
        fence_posts_x = [np.percentile(lens_data[cols[0]], post) for post in np.arange(perc_step, 100, perc_step)]
        fence_posts_y = [np.percentile(lens_data[cols[1]], post) for post in np.arange(perc_step, 100, perc_step)]

        lower_bound_x = np.array([xmin] + fence_posts_x)
        upper_bound_x = np.array(fence_posts_x + [xmax])
        lower_bound_y = np.array([ymin] + fence_posts_y)
        upper_bound_y = np.array(fence_posts_y + [ymax])
        
        widths_x = upper_bound_x - lower_bound_x
        spill_over_x = gain * widths_x
        lower_bound_x = lower_bound_x - spill_over_x
        upper_bound_x = upper_bound_x + spill_over_x
        widths_y = upper_bound_y - lower_bound_y
        spill_over_y = gain * widths_y
        lower_bound_y = lower_bound_y - spill_over_y
        upper_bound_y = upper_bound_y + spill_over_y
        
        for i in range(resolution):
            for j in range(resolution):
                patch = list(lens_data[(lens_data[cols[0]] > lower_bound_x[i]) &
                                    (lens_data[cols[0]] < upper_bound_x[i]) &
                                    (lens_data[cols[1]] > lower_bound_y[j]) &
                                    (lens_data[cols[1]] < upper_bound_y[j])
                                   ].index)
                key = ((round(lower_bound_x[i], 2), round(upper_bound_x[i], 2)),
                    (round(lower_bound_y[j], 2), round(upper_bound_y[j], 2)))
                patch_dict[key] = patch
        return patch_dict
    
    else:
        width_x = (xmax - xmin) / resolution
        width_y = (ymax - ymin) / resolution
        spill_over_x = gain * width_x
        spill_over_y = gain * width_y

        lower_bound_x = np.arange(xmin, xmax, width_x) - spill_over_x
        upper_bound_x = np.arange(xmin, xmax, width_x) + width_x + spill_over_x
        lower_bound_y = np.arange(ymin, ymax, width_y) - spill_over_y
        upper_bound_y = np.arange(ymin, ymax, width_y) + width_y + spill_over_y
        for i in range(resolution):
            for j in range(resolution):
                patch = list(lens_data[(lens_data[cols[0]] > lower_bound_x[i]) &
                                    (lens_data[cols[0]] < upper_bound_x[i]) &
                                    (lens_data[cols[1]] > lower_bound_y[j]) &
                                    (lens_data[cols[1]] < upper_bound_y[j])
                                   ].index)
                key = ((round(lower_bound_x[i], 2), round(upper_bound_x[i], 2)),
                    (round(lower_bound_y[j], 2), round(upper_bound_y[j], 2)))
                patch_dict[key] = patch
        return patch_dict


def optimal_clustering(df, patch, method='kmeans', min_patch_N=50):
    K_max = int(min_patch_N / 10)
    if method == 'kmeans':
        clustering = {}
        db_index = []
        X = df.ix[patch,:]
        for k in range(1, K_max):
            kmeans = cluster.KMeans(n_clusters=k).fit(X)
            clustering[k] = pd.DataFrame(kmeans.predict(X), index=patch)
            dist_mu = squareform(pdist(kmeans.cluster_centers_))
            sigma = []
            for i in range(k):
                points_in_cluster = clustering[k][clustering[k][0] == i].index
                sigma.append(sqrt(X.ix[points_in_cluster,:].var(axis=0).sum()))
            db_index.append(davies_bouldin(dist_mu, np.array(sigma)))
        db_index = np.array(db_index[1:])
        k_optimal = np.argmin(db_index) + 2
        return [list(clustering[k_optimal][clustering[k_optimal][0] == i].index) for i in range(k_optimal)]
    
    elif method == 'agglomerative':
        clustering = {}
        db_index = []
        X = df.ix[patch,:]
        for k in range(1, K_max):
            agglomerative = cluster.AgglomerativeClustering(n_clusters=k, linkage='average').fit(X)
            clustering[k] = pd.DataFrame(agglomerative.fit_predict(X), index=patch)
            tmp = [list(clustering[k][clustering[k][0] == i].index) for i in range(k)]
            centers = np.array([np.mean(X.ix[c,:], axis=0) for c in tmp])
            dist_mu = squareform(pdist(centers))
            sigma = []
            for i in range(k):
                points_in_cluster = clustering[k][clustering[k][0] == i].index
                sigma.append(sqrt(X.ix[points_in_cluster,:].var(axis=0).sum()))
            db_index.append(davies_bouldin(dist_mu, np.array(sigma)))
        db_index = np.array(db_index[1:])
        k_optimal = np.argmin(db_index) + 2
        return [list(clustering[k_optimal][clustering[k_optimal][0] == i].index) for i in range(k_optimal)]
    
    else:
        raise 'error: only k-means and agglomerative clustering are supported'


def mapper_graph(df, lens='pca', resolution=10, gain=0.5, equalize=True, clust='kmeans', min_patch_occupancy=50):
    '''
    input: N x n_dim image of of raw data under lens function, as a dataframe
    output: (undirected graph, list of node contents) 
    '''
    lens_data = apply_lens(df, lens=lens)
    
    patch_clusterings = {}
    counter = 0
    for key, patch in covering_patches(lens_data, resolution=resolution, gain=gain, equalize=equalize).items():
        if len(patch) > min_patch_occupancy:
            patch_clusterings[key] = optimal_clustering(df, patch, method=clust, min_patch_N=min_patch_occupancy)
            counter += 1
    print 'total of {} patches required clustering'.format(counter)

    all_clusters = []
    for key in patch_clusterings:
        all_clusters += patch_clusterings[key]
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


