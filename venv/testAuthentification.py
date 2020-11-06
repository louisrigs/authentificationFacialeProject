import unittest
import matplotlib.pyplot as plt
import dataLoad as load
from authentification import bfAuth
import brute_force_search as bfs

index = 99
radius = 2000000


class MyTestCase(unittest.TestCase):
	#load.dataLoad()
	def test_dataLoad(self):
		tailleGal = len(load.gallery)
		taillePro = len(load.probes1) + len(load.probes2)
		tailleGro = len(load.groundtruth)
		self.assertEqual(taillePro + tailleGal, tailleGro)

	def test_auth_brute(self):
		voisins = bfs.radius_search(load.gallery, load.probes1[index], radius)[0]
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

		self.assertEqual(bfAuth(load.probes1[index], load.gallery), True)
		print(bfs.radius_search(load.gallery, load.probes2[index], radius)[0])
		self.assertEqual(bfAuth(load.probes2[index], load.gallery), False)
		print(bfs.radius_search(load.groundtruth, load.probes2[index], radius)[0])
		self.assertEqual(bfAuth(load.probes2[index], load.groundtruth), True)
		print(bfs.radius_search(load.groundtruth, load.probes1[index], radius)[0])
		self.assertEqual(bfAuth(load.probes1[index], load.groundtruth), True)


if __name__ == '__main__':
	unittest.main()
