import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import img
from authentification import bfAuth

maxprobes = 100

gallery = []
probes = []
groundtruth = []
probes1 = []
probes2 = []

def dataLoad(n):
	# path = "C:/Users/benoît/Documents/IMT Lille Douai/M1/ODATA/Projet/ODATA_project_authentication_data/data/dataset1"
	path = "D:/louis/Documents/Institut Mines-Télécom Lille-Douai 2017-2023/4-M1 - 2020-2021/Modules/P2 - ODATA - Outils pour la Data Science/Projet Authentification faciale/data/dataset1/images"
	print("Chargement des données en cours... patientez")

	currentName = ''
	compteur = 0
	for root, _, files in os.walk(path):
		current_directory_path = os.path.abspath(root)
		for f in files:
			nameVersion, ext = os.path.splitext(f)
			if ext == ".jpg":
				current_image_path = os.path.join(current_directory_path, f)
				current_image = mpimg.imread(current_image_path)
				name, version = os.path.splitext(nameVersion)
				groImg = img.image(name,version,current_image)

				if len(probes2) < maxprobes:
					probes2.append(current_image)
					groundtruth.append(groImg)
				else:
					if len(probes1) < maxprobes:
						if name == currentName:
							if compteur < n:
								probes1.append(current_image)
								groundtruth.append(groImg)
								compteur += 1
							else:
								gallery.append(current_image)
								groundtruth.append(groImg)
						else:
							compteur = 1
							probes1.append(current_image)
							groundtruth.append(groImg)
							currentName = name
					else:
						gallery.append(current_image)
						groundtruth.append(groImg)

	for l in probes1:
		probes.append(l)
	for l in probes2:
		probes.append(l)

	print("Gallery : ", len(gallery), "\tProbes : ", len(probes), "\tGroundtruth : ", len(groundtruth))
	print("Chargement des images: complété")