import dataLoad as load
import authentification as auth
import numpy as np

load.dataLoad(2)
gallery = load.gallery
probes = load.probes
groundTruth = load.groundtruth

def casSuccErr(radius):
	bfCas1 = []
	bfCas2 = []
	bfCas3 = []
	bfCas4 = []
	for i in range (0,100):
		bfCas1.append(auth.bfAuth(probes[i], gallery, radius))
		bfCas2.append(auth.bfAuth(probes[i+100], gallery, radius))
	return bfCas1,bfCas2

#cas1, cas2 = casSuccErr(1300000)
#print(cas1,"\n", cas2)

def evaluate(image):
	identity = ''
	autres = []
	autresMat = []
	i = 0
	enregistre = False
	for l in groundTruth:
		i += 1
		comparaison = l.matrix == image
		if comparaison.all():
			identity = l.name
			enregistre = True
			print(identity)
			break

	if enregistre == True:
		for l in groundTruth:
			if identity == l.name:
				autresNom.append(identity + l.version)
				autresMat.append(l.matrix)

	print("Identité de l'individu:")
	print(autresNom)

	return inData,identity,autresNom,autresMat

#enregistre, identite, autresNom, autresMat, = evaluate(gallery[600])

# TP - Vrai positif : cas 1 : autorise à un utilisateur justement enregistré
# FP - Faux positif : cas 2 : autorise à utilisateur enregistré, mais par mauvaise reconaissance
# FP - Faux positif : cas 3 : autorise à utilisateur non-enregistré, mais par reconaissance proche
# TN - Vrai négatif : cas 4 : refuse à un utilisateur non-enregistré
# FN - Faux négatif : cas 5 : refuse à un utilisateur justement enregistré
#
def evalMesure(image,dataset,radius):
	enregistre, identite,autres,autresMat = evaluate(image)
	voisinsProches = auth.bfs.radius_search(dataset,image,radius)[0]
	authentifie = auth.bfAuth(image,dataset,radius)
	TP, FP, TN, FN = 0

	image_reconnue = False
	for i in range(0, len(voisinsProches)):
		for j in range(0, len(autresMat)):
			if dataset[voisinsProches[i]] != autresMat[j]:
				continue
			else:
				image_reconue = True
				break

	if authentifie == True:
		if enregistre == True:
			if image_reconnue == True:  # cas 1
				TP = 1
			else:   # cas 2
				FP = 1
		else:
			FP = 1
	else:
		if enregistre == True:
			FN = 1
		else:
			TN = 1
	return [TP,FP,FN,TN]

def exactitude(TP,FP,FN,TN):
	return (TP+TN)/(TP+FP+FN+TN)

def precision(TP,FP,FN,TN):
	return TP/(TP+FP)

def sensi(TP,FP,FN,TN):
	return TP/(TP+FN)

def specif(TP,FP,FN,TN):
	return TN/(FP+TN)

