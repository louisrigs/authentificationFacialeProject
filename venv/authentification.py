import brute_force_search as bfs
import eigenFaces as eigF

radius = 2000000
def bfAuth(image, dataset):
	voisins_proche = bfs.radius_search(dataset, image, radius)[0]
	if len(voisins_proche) > 0 :
		return True
	else:
		return False


def eigenAuth(image,dataset):

	eigFacValP,eigenFaces,composantes,imgComp = eigF.eigenFaces(image,dataset)
	print(composantes)
	print(imgComp)
"""
	bfs.radius_search(composantes,image,radius)[0]
"""