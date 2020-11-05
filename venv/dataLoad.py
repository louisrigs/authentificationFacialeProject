import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import img
from authentification import auth
from sklearn.decomposition import PCA

n = 3
maxprobes = 100

gallery = []
probes = []
groundtruth = []
probes1 = []
probes2 = []


def dataLoad():
	# path = "C:/Users/benoît/Documents/IMT Lille Douai/M1/ODATA/Projet/ODATA_project_authentication_data/data/dataset1"
	path = "D:/louis/Documents/Institut Mines-Télécom Lille-Douai 2017-2023/4-M1 - 2020-2021/Modules/P2 - ODATA - Outils pour la Data Science/Projet Authentification faciale/data/dataset1/images"

	currentName = ''
	compteur = 0

	print('Selection des fichiers .jpg...\n', 'n=', n, end='')

	for root, _, files in os.walk(path):
		current_directory_path = os.path.abspath(root)
		for f in files:
			nameVersion, ext = os.path.splitext(f)
			if ext == ".jpg":
				current_image_path = os.path.join(current_directory_path, f)
				current_image = mpimg.imread(current_image_path)

				name, version = os.path.splitext(nameVersion)
				images = img.image(name, version, current_image)

				if len(probes2) < maxprobes:
					probes2.append(current_image)
					groundtruth.append(current_image)
				# groundtruth.append(images)
				else:
					if len(probes1) < maxprobes:
						if name == currentName:
							if compteur < n:
								probes1.append(current_image)
								groundtruth.append(current_image)
								# groundtruth.append(images)
								compteur += 1
							else:
								gallery.append(current_image)
								groundtruth.append(current_image)
						# groundtruth.append(images)
						else:
							compteur = 1
							probes1.append(current_image)
							groundtruth.append(current_image)
							# groundtruth.append(images)
							currentName = name
					else:
						gallery.append(current_image)
						groundtruth.append(current_image)
						# groundtruth.append(images)

	probes = probes1 + probes2

	print("Taille de gallery : ", len(gallery), "\nTaille de probes : ", len(probes), "\nTaille de groundtruth : ",
	      len(groundtruth))
	print("Chargement des images: complété")
