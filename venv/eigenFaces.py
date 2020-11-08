from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import dataLoad as load
import numpy as np

composantes = []
compList = []

def eigenFaces(image, dataset, nbrAxes):
	galV = np.array([l.flatten() for l in dataset])             #linéarisation des images en vecteurs
	galVY = galV - np.mean(galV, axis=0)

	imgV = np.array(image.flatten())
	imgVy = imgV - np.mean(galV, axis=0)
	imgComp = []

	print("Enclenchement du PCA...", end='')
	covDT = np.cov(galVY)
	print("Covariance créee...")
	eigFacValPrp, eigenFacVecPro = np.linalg.eigh(covDT)  # ACP sur les données centrées réduites
	eigenPrincip = []
	for i in range(0,len(eigenFacVecPro)):
		vecPrincip = np.dot(galVY.T, eigenFacVecPro[i])
		eigenPrincip.append(vecPrincip)
	print("Vecteurs crées")

	for l in eigenPrincip:
		norm = np.linalg.norm(l)
		if norm !=0:
			l = l/norm

	print("Vecteurs normalisés")
	"""
	print("Enclenchement du PCA...", end='')
	pca = PCA()
	pca.fit(galVY)
	eigenFaces = pca.components_  # chaque ligne est un vecteur propre
	eigFacValP = pca.explained_variance_  # valeurs propres par ordre décroissant
	print("complété")
	"""

	"""
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

	imgMatComp = imgComp
	galMatcomp = np.array([np.array(xi) for xi in composantes],dtype="object")

	longueur = len(galMatcomp[0])

	for i in range(0,longueur):
		mat = np.zeros((nbrAxes))
		for j in range(0,nbrAxes):
			mat[j] = galMatcomp[j][i]
		compList.append(mat)
	"""

	return eigenPrincip,imgVy
	#return compList,imgMatComp


"""plt.figure()
	plt.title("Carte des individus")
	plt.xlim(c1.min()-5, c1.max()+5)
	plt.ylim(c2.min()-5, c2.max()+5)
	plt.axis("on")
	plt.scatter(c1, c2, s=10, c='red', marker='+')
	plt.show()"""