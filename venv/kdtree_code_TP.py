# -*- coding: utf-8 -*-
"""
Created on Tue Oct 20 15:22:16 2020

@author: louis
"""
import numpy as np
import kdtree
import brute_force_search as bfs
import timeit

dataset_glove = np.load(
    'D:/louis/Documents/Institut Mines-Télécom Lille-Douai 2017-2023/4-M1 - 2020-2021/Modules/P2 - ODATA - Outils pour la Data Science/Recherche par similarité/ODATA - Recherche par similarité - TP/glove_200d/dataset_glove_200d.npy')
dataset_word_glove = np.load(
    'D:/louis/Documents/Institut Mines-Télécom Lille-Douai 2017-2023/4-M1 - 2020-2021/Modules/P2 - ODATA - Outils pour la Data Science/Recherche par similarité/ODATA - Recherche par similarité - TP/glove_200d/dataset_words_glove_200d.npy')
probes_glove = np.load(
    'D:/louis/Documents/Institut Mines-Télécom Lille-Douai 2017-2023/4-M1 - 2020-2021/Modules/P2 - ODATA - Outils pour la Data Science/Recherche par similarité/ODATA - Recherche par similarité - TP/glove_200d/probes_glove_200d.npy')
probes_words_glove = np.load(
    'D:/louis/Documents/Institut Mines-Télécom Lille-Douai 2017-2023/4-M1 - 2020-2021/Modules/P2 - ODATA - Outils pour la Data Science/Recherche par similarité/ODATA - Recherche par similarité - TP/glove_200d/probes_words_glove_200d.npy')


def index_init():
    print("\nInitialisation du kd-tree...", end='')
    index = kdtree.KDTree()
    index.__init__()
    print("100%")
    print("Construction du kd-tree...", end='')
    index.build(dataset_glove)
    print("100%")
    return index


index = index_init()


def search_meth():
    search_BT = \
    index.search(query=probes_glove[4], max_visited_leaves=5000, branch_and_bound=False, best_bin_first=False)[1]
    search_BB = \
    index.search(query=probes_glove[4], max_visited_leaves=5000, branch_and_bound=True, best_bin_first=False)[1]
    search_BBF = \
    index.search(query=probes_glove[4], max_visited_leaves=5000, branch_and_bound=True, best_bin_first=True)[1]
    return search_BT, search_BB, search_BBF


# search_meth()


# precision : pour chaque requête, trouver un certain nombres de voisins (k),
# stocker les k nombres de voisins, comparer avec la bruteforce search

def acceleration(temps1, temps2):
    return temps1 - temps2


def calculs_une_req():
    search_BT = search_meth()[0]
    search_BB = search_meth()[1]
    search_BBF = search_meth()[2]
    search_BFS = bfs.knn_search(dataset_glove, probes_glove[4])[0]

    precis_BT = np.in1d(search_BT, search_BFS)
    precis_BB = np.in1d(search_BB, search_BFS)
    precis_BBF = np.in1d(search_BBF, search_BFS)

    print('Precision BT', precis_BT)
    print('Precision BB', precis_BB)
    print('Precision BBF', precis_BBF)

    tempsBT = timeit.timeit(index.search(query=probes_glove[4], max_visited_leaves=5000, branch_and_bound=False,
                                         best_bin_first=False)) / 100
    tempsBB = timeit.timeit(
        index.search(query=probes_glove[4], max_visited_leaves=5000, branch_and_bound=True, best_bin_first=False)) / 100
    tempsBBF = timeit.timeit(
        index.search(query=probes_glove[4], max_visited_leaves=5000, branch_and_bound=True, best_bin_first=True)) / 100
    tempsBFS = timeit.timeit(bfs.knn_search(dataset_glove, probes_glove[4])) / 100

    accelerationBT = acceleration(tempsBFS, tempsBT)
    accelerationBB = acceleration(tempsBFS, tempsBB)
    accelerationBBF = acceleration(tempsBFS, tempsBBF)

    print("\nAcceleration BT:", accelerationBT)
    print("\nAcceleration BB:", accelerationBB)
    print("\nAcceleration BBF:", accelerationBBF)


"""
def comparaisonprecision():
    print("Initialisation du KDTree ......")
    index = kdtree.KDTree()
    print("Initialisation du KDTree effectuée.")
    print("Construction du KDTree ......")
    index.build(datavectors)
    print("Construction du KDTree effectuée.")

    matPrecisionBT = []
    for i in range(len(probesvectors)):
        print("BT : {}".format(i))
        resbacktracking = index.search(query = probesvectors[i], k = 10, max_visited_leaves = 5000, branch_and_bound=False, best_bin_first=False)[1]

        resbfs = bfs.knn_search(datavectors, probesvectors[i], datawords, k = 10)[0]

        comparaison = np.in1d(resbacktracking, resbfs)

        precision = np.sum((comparaison)/10*100)
        print(precision)
        matPrecisionBT.append(precision)
    moyBT = np.sum(matPrecisionBT)/100

#4.9


    matPrecisionBAB = []
    for i in range(len(probesvectors)):
        print("BAB : {}".format(i))
        resbranchandbound = index.search(query = probesvectors[i], k = 10, max_visited_leaves = 5000, branch_and_bound=True, best_bin_first=False)[1]

        resbfs = bfs.knn_search(datavectors, probesvectors[i], datawords, k = 10)[0]

        comparaison = np.in1d(resbranchandbound, resbfs)

        precision = np.sum((comparaison)/10*100)
        print(precision)
        matPrecisionBAB.append(precision)
    moyBAB = np.sum(matPrecisionBAB)/100

    #4.9

    matPrecisionBBF = []

    for i in range(len(probesvectors)):
        print("BBF : {}".format(i))
        resbestbindfirst = index.search(query = probesvectors[i], k = 10, max_visited_leaves = 5000, branch_and_bound=True, best_bin_first=True)[1]

        resbfs = bfs.knn_search(datavectors, probesvectors[i], datawords, k = 10)[0]

        comparaison = np.in1d(resbestbindfirst, resbfs)

        precision = np.sum((comparaison)/10*100)
        print(precision)
        matPrecisionBBF.append(precision)
    moyBBF = np.sum(matPrecisionBBF)/100

#12.1

    return moyBBF
"""

calculs_une_req()