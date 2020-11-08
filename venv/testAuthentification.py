import unittest
import matplotlib.pyplot as plt
import dataLoad as load
from authentification import bfAuth,eigenAuth
import brute_force_search as bfs
import eigenFaces as eigF

index = 50
radius = 1100000


class MyTestCase(unittest.TestCase):
	load.dataLoad(2)

	"""	
	def test_dataLoad(self):
		tailleGal = len(load.gallery)
		taillePro = len(load.probes)
		tailleGro = len(load.groundtruth)
		self.assertEqual(taillePro + tailleGal, tailleGro)
		"""
	"""	
	def test_auth_brute(self):
		voisins = bfs.radius_search(load.gallery, load.probes[index], radius)[0]
		print(voisins)
		plt.figure()
		plt.title("Probes")
		plt.axis("off")
		plt.imshow(load.probes1[index])
		plt.show()

		for l in voisins:
			plt.figure()
			plt.title("groundtruth ")
			plt.axis("off")
			plt.imshow(load.gallery[l])
			plt.show()

		self.assertEqual(bfAuth(load.probes[index], load.gallery,radius), True)

		print(bfs.radius_search(load.groundtruth, load.probes[index], radius)[0])
		self.assertEqual(bfAuth(load.probes[index], load.groundtruth, radius), True)

		print(bfs.radius_search(load.gallery, load.probes2[index], radius)[0])
		self.assertEqual(bfAuth(load.probes2[index], load.gallery,radius), False)

		print(bfs.radius_search(load.groundtruth, load.probes2[index], radius)[0])
		self.assertEqual(bfAuth(load.probes2[index], load.groundtruth,radius), True)
		"""

	def test_auth_eigen(self):
		"""eigFacValP, eigenFaces, compList, imgMatComp = eigF.eigenFaces(load.probes[index], load.gallery)
		voisins = bfs.radius_search(compList, imgMatComp, radius)[0]
		print("Voisins proches de probes : ",voisins)"""

		print("Tests eigenAuth :")

		#self.assertEqual(eigenAuth(load.probes[index], load.gallery, radius), True)

		self.assertEqual(eigenAuth(load.probes1[index+100], load.gallery, radius), False)
		print("Ok")
		"""
		eigFacValP, eigenFaces, compMat, imgMatComp = eigF.eigenFaces(load.probes[index], load.groundtruth)
		print("Probes 1 dans groundtruth :")
		print(bfs.radius_search(compMat, imgMatComp, radius)[0])
		print("Probes 1 dans groundtruth :")

		eigFacValP, eigenFaces, compMat, imgMatComp = eigF.eigenFaces(load.probes2[index], load.gallery)
		print("Probes 2 dans gallery :")
		print(bfs.radius_search(compMat, imgMatComp, radius)[0])
		self.assertEqual(eigenAuth(load.probes2[index], load.gallery, radius), False)

		eigFacValP, eigenFaces, compMat, imgMatComp = eigF.eigenFaces(load.probes2[index], load.groundtruth)
		print("Probes 2 dans groundtruth :")
		print(bfs.radius_search(compMat, imgMatComp, radius)[0])
		self.assertEqual(eigenAuth(load.probes2[index], load.groundtruth, radius), True)
		"""


if __name__ == '__main__':
	unittest.main()
