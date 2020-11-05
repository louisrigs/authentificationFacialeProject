import dataLoad as load
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
from sklearn.decomposition import PCA
from authentification import auth


load.dataLoad()
"""
imageeee = mpimg.imread("D:/louis/Documents/Institut Mines-Télécom Lille-Douai 2017-2023/4-M1 - 2020-2021/Modules/P2 - ODATA - Outils pour la Data Science/Projet Authentification faciale/data/dataset1/images/9326871.1.jpg")
imgY = imageeee - np.mean(imageeee,axis=0)
covImg = np.cov(imgY, rowvar=0)
valp, vecp = np.linalg.eig(covImg)

pca = PCA(n_components=150)
pca.fit(imgY)
valp2 = pca.explained_variance_
vecp2 = pca.components_
"""
"""

plt.figure()
plt.title("Probes")
plt.axis("off")
plt.imshow(load.probes1[index])
plt.show()


for l in voisins_proches:
	plt.figure()
	plt.title("groundtruth ")
	plt.axis("off")
	plt.imshow(load.gallery[l])
	plt.show()

print("affichage des voisins complété")"""