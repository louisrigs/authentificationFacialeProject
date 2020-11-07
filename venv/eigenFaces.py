from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import dataLoad as load
import numpy as np

nbrAxes = 3
composantes = []
compMat = []

def eigenFaces(image, dataset):
	galV = np.array([l.flatten() for l in dataset])             #linéarisation des images en vecteurs
	galVY = galV - np.mean(galV, axis=0)

	imgV = image.flatten()
	imgVy = imgV - np.mean(imgV, axis=0)
	imgComp = []

	print("Enclenchement du PCA...", end='')
	pca = PCA()
	pca.fit(galVY)              # ACP sur les données centrées réduites
	print("complété")
	print("Création des vecteurs propres de l'ACP")
	eigenFaces = pca.components_ # chaque ligne est un vecteur propre
	eigFacValP = pca.explained_variance_ #valeurs propres par ordre décroissant

	for i in range(0,nbrAxes):
		eigFi = eigenFaces[i]
		normPi = np.linalg.norm(eigFi)
		if normPi != 0:
			eigFNi = eigFi/normPi
			comp_i = np.dot(galVY,eigFNi.T)
			composantes.append(comp_i)
			imgComp.append(np.dot(imgVy, eigFNi.T))
		else:
			comp_i = np.dot(galVY,eigFi.T)
			composantes.append(comp_i)
			imgComp.append(np.dot(imgVy, eigFi.T))
		print("Moyenne composante ",i+1,' :', np.mean(comp_i))
		print("Variance composante ",i+1,' :', np.var(comp_i))

	compMat = np.matrix(composantes[0].T)
	"""for i in range(1,len(composantes)):
		aconcat = np.matrix(np.matrix(composantes[i].T))
		matcomp = compMat
		compMat = np.hstack(matcomp,aconcat)"""

	return eigFacValP,eigenFaces,compMat,imgComp


"""print("Enclenchement du scaler...")
	scaler = StandardScaler()
	scaler.fit(galV)
	galVZ = scaler.transform(galV)  """    # données centrées réduites

"""

partInertie = pca.explained_variance_ratio_ # part d'inertie par chaque axe
partInertieCumul = np.cumsum(pca.explained_variance_ratio_) # part d'inertie cumulée"""

"""plt.figure()
	plt.title("Carte des individus")
	plt.xlim(c1.min()-5, c1.max()+5)
	plt.ylim(c2.min()-5, c2.max()+5)
	plt.axis("on")
	plt.scatter(c1, c2, s=10, c='red', marker='+')
	plt.show()"""