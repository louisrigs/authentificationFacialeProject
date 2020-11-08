import brute_force_search as bfs
import eigenFaces as eigF

def bfAuth(image,dataset,radius):
	voisins_proche = bfs.radius_search(dataset, image, radius)[0]

	#print("Nbr voisins: ", len(voisins_proche), "\tvoisins :", voisins_proche, "\tradius :", radius)

	if len(voisins_proche) > 0 :
		return True
	else:
		return False

def eigenAuth(image,dataset,radius):
	compList, imgMatComp = eigF.eigenFaces(image, dataset,2)
	voisins_proche = bfs.radius_search(compList,imgMatComp,radius)[0]

	#print("Nbr voisins: ", len(voisins_proche), "\tvoisins :", voisins_proche, "\tradius :", radius)

	if len(voisins_proche) > 0:
		return True
	else:
		return False