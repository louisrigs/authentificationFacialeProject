import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

n = 2
maxprobes = 100


def dataLoad():
	# path = "C:/Users/benoît/Documents/IMT Lille Douai/M1/ODATA/Projet/ODATA_project_authentication_data/data/dataset1"
	path = "D:/louis/Documents/Institut Mines-Télécom Lille-Douai 2017-2023/4-M1 - 2020-2021/Modules/P2 - ODATA - Outils pour la Data Science/Projet Authentification faciale/data/dataset1/images"

	gallery = []
	probes = []
	probes1 = []
	probes2 = []

	compteur = 0
	currentName = ''

	print('Selection des fichiers .jpg...\n', end='')

	for root, _, files in os.walk(path):
		current_directory_path = os.path.abspath(root)

		for f in files:

			nameVersion, ext = os.path.splitext(f)
			if ext == ".jpg":
				current_image_path = os.path.join(current_directory_path, f)
				current_image = mpimg.imread(current_image_path)
				name, version = os.path.splitext(nameVersion)

				if len(probes2) < maxprobes:
					probes2.append(current_image)
					print(name)
				else:
					if len(probes1) < maxprobes:
						if name == currentName:
							if compteur <= n:
								probes1.append(current_image)
							else:
								gallery.append(current_image)
							compteur += 1
						else:
							if compteur <= n:
								probes1.append(current_image)
							else:
								gallery.append(current_image)
							compteur = 1
							currentName = name

					else:
						gallery.append(current_image)




	print('100%\n', end='')

	print(len(probes1))
	print(len(probes2))
	print(len(gallery))

	iter = 0
	for image in probes1:
		if iter <= 10:
			plt.figure()
			plt.axis("off")
			plt.imshow(image)
			plt.show()
		iter += 1

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
