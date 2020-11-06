import dataLoad as load
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

load.dataLoad()

gallery = []
probes = []
groundTruth = []
vecPropres = []

gallery = load.gallery
probes = load.probes1 + load.probes2
groundTruth = load.groundtruth

scaler = StandardScaler()
scaler.fit(gallery[0])
Z = scaler.transform(gallery[0])
Z_moy = np.mean(Z)  #proche de 0
Z_var = np.var(Z)   #proche de 1 (valeur centrée réduite)
print('\n Moyenne de Z :', Z_moy, '\n Variance de Z :', Z_var)

X_moy = np.mean(groundTruth[0],axis=0)
matY = groundTruth - X_moy

pca = PCA()
pca.fit(Z)
vecPropres = pca.components_ # chaque ligne est un vecteur propre
valPropres = pca.explained_variance_ #valeurs propres par ordre décroissant
partInertie = pca.explained_variance_ratio_
partInertieCumul = np.cumsum(pca.explained_variance_ratio_)
