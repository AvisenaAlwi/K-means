import numpy as np
import pandas as pd
import sys
import matplotlib.pyplot as plt
from math import sqrt

def is_equal(array1, array2):
    equal = True
    try:
        for i in range(0, len(array1)):
            for j in range(0, len(array1[1]) - 1):
                if not np.array_equal(array1[i][j] , array2[i][j] ) :
                    return False
        return True
    except:
        return False

def min_max_normalisasi(data) :
    for i in range(0,4) :
        v = data[:,i]
        data[:, i] = (v - v.min()) / (v.max() - v.min())

def distance(data1, data2):
    sum = 0
    for i in range(0, len(data1)):
        sum += abs( data1[i] - data2[i] )
    return sqrt(sum)

def centroid(data_array):
    count_data = len( data_array )
    count_column = len( data_array[0] )
    centroid = []
    data_array = np.array(data_array)
    for i in range(0, count_column) :
        mean = np.sum(data_array[: , i]) / count_data
        centroid.append(mean)
    return centroid

def get_centroids(data_array):
    centroids = []
    for i in range(0, len(data_array)):
        centroids.append( centroid( data_array[i] ) )
    return centroids


def main() :
    # nama file
    file_name = 'Soal Clustering.xlsx'
    # baca file excel
    df = pd.read_excel(file_name, sheet_name='Sheet1')
    # masukkan data nilainya ke numpy ndarray variable data
    data = df.values[:,1:]

    # banyak clusternya
    if len(sys.argv) == 1 :
        print("Error minimal 2 cluster")
        return
    else:
        N = int(sys.argv[1])
    
    print("Banyak Cluster adalah :", N)
    # STEP 1 : Normalisasi data
    min_max_normalisasi(data)
    
    # STEP 2 : INIT cluster secara random
    N_data = len(data)
    N_data_in_cluster = int(N_data / N)
    data_cluster = np.array_split( data , N )

    # STEP 3 : HITUNG MASING MASING CLUSTER
    w, h = 0, N
    result_clustering = [[0 for x in range(w)] for y in range(h)] 

    max_loop = 10
    loop = 0
    moving = True
    last_data_cluster = np.copy( data_cluster )
    while moving :
        w, h = 0, N
        result_clustering = [[0 for x in range(w)] for y in range(h)] 
        centroids = get_centroids(data_cluster)
        last_data_cluster = np.copy( data_cluster )
        w, h = 0, N
        data_cluster = [[np.array([]) for x in range(w)] for y in range(h)]
        for i in range(0, N_data):
            distances = []
            for j in range( 0, len( centroids ) ) :
                distances.append( distance( data[i], centroids[j] ) )
            cluster = distances.index( np.min(distances) )
            result_clustering[cluster].append(i)
            data_cluster[cluster].append( data[i] )

        loop += 1
        if is_equal(last_data_cluster , data_cluster) or loop >= max_loop:
            moving = False

        print("Loop", loop,":")
        for i in range(0, N):
            print("Data pada cluster ",i+1,result_clustering[i])
    print("\n==== HASIL AKHIR ====")
    for i in range(0, N):
            print("Data pada cluster ",i+1,result_clustering[i])


main()