import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

def dataLoad():
	print('Mise en place du path...',end='')
	images = []
	path = "D:/louis/Documents/Institut Mines-Télécom Lille-Douai 2017-2023/4-M1 - 2020-2021/Modules/P2 - ODATA - Outils pour la Data Science/Projet Authentification faciale/data/dataset1/images"
	print('100%\n', end='')

	print('Selection des fichiers .jpg...', end='')
	for root, _, files in os.walk(path):
		current_directory_path = os.path.abspath(root)
		for f in files:
			name, ext = os.path.splitext(f)
			print('nom',name)

			if ext == ".jpg":
				current_image_path = os.path.join(current_directory_path,f)
				current_image = mpimg.imread(current_image_path)
				images.append(current_image)

	print('100%\n',end='')

	print('Affichage des images ...',end='')

	iter=0
	for img in images:
		iiter += 1
		plt.figure()
		plt.axis("off")
		plt.imshow(img)
		plt.show()
		if iter == 15:
			break

	print('100%\n',end='')


dataLoad()


