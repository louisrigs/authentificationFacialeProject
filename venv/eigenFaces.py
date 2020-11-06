from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import dataLoad as load
import numpy as np

def eigenFaces():
	### changer probes1 par gallery
	galV = np.array([l.flatten() for l in load.gallery])             #linéarisation des images en vecteurs

	print("Enclenchement du scaler...")
	scaler = StandardScaler()
	scaler.fit(galV)
	galVZ = scaler.transform(galV)      # données centrées réduites

	print("Enclenchement du PCA...", end='')
	pca = PCA()
	pca.fit(galVZ)              # ACP sur les données centrées réduites
	print("complété")
	print("Création des vecteurs propres de l'ACP")
	vecPropres = pca.components_ # chaque ligne est un vecteur propre
	valPropres = pca.explained_variance_ #valeurs propres par ordre décroissant
	partInertie = pca.explained_variance_ratio_ # part d'inertie par chaque axe
	partInertieCumul = np.cumsum(pca.explained_variance_ratio_) # part d'inertie cumulée

	v1 = vecPropres[0]
	v2 = vecPropres[1]
	normalV1 = np.linalg.norm(v1)
	normalV2 = np.linalg.norm(v2)

	if normalV1 != 0:
		V1 = vecPropres[0] / normalV1
		V2 = vecPropres[1] / normalV2

	c1 = np.dot(galVZ, v1.T)
	c2 = np.dot(galVZ, v2.T)

	print(np.mean(c1), np.mean(c2))
	print(np.var(c1), np.var(c2))

	plt.figure()
	plt.title("Carte des individus")
	plt.xlim(c1.min(), c1.max())
	plt.ylim(c2.min(), c2.max())
	plt.axis("on")
	plt.scatter(c1, c2, s=10, c='red', marker='+')
	plt.show()

	return valPropres,vecPropres,c1,c2