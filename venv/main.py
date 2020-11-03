import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

def dataLoad():
	#path = "C:/Users/benoît/Documents/IMT Lille Douai/M1/ODATA/Projet/ODATA_project_authentication_data/data/dataset1"
	path = "D:/louis/Documents/Institut Mines-Télécom Lille-Douai 2017-2023/4-M1 - 2020-2021/Modules/P2 - ODATA - Outils pour la Data Science/Projet Authentification faciale/data/dataset1/images"

	gallery = []
	probes = []
	names = []

	iteration = 0
	compteur = 0
	currentName = ''

	print('Selection des fichiers .jpg...\n', end='')

	for root, _, files in os.walk(path):
		current_directory_path = os.path.abspath(root)

		for f in files:

			nameVersion, ext = os.path.splitext(f)
			if ext == ".jpg":
				name, version = os.path.splitext(nameVersion)

				if name == currentName:
					compteur += 1
					print(name)
					print(compteur)
				else:
					currentName = name
					compteur = 1
					print(name)
					print(compteur)
				iteration += 1

				"""	
				current_image_path = os.path.join(current_directory_path,f)
				current_image = mpimg.imread(current_image_path)

				gallery.append(current_image)
				"""



	print('100%\n',end='')


	"""
	print('Affichage des images ...',end='')
	
	iter = 0
	for image in gallery:
		iter += 1
		plt.figure()
		plt.axis("off")
		plt.imshow(image)
		plt.show()
		if iter == 100:
			break

	print('100%\n',end='')
"""

dataLoad()


