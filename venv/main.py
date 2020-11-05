import dataLoad as load
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
#from sklearn.decomposition import PCA



img = mpimg.imread("D:/louis/Documents/Institut Mines-Télécom Lille-Douai 2017-2023/4-M1 - 2020-2021/Modules/P2 - ODATA - Outils pour la Data Science/Projet Authentification faciale/data/dataset1/images/9326871.1.jpg")
img = img - np.mean(img,axis=0)
covImg = np.cov(img, rowvar=0)
valp, vecp = np.linalg.eig(covImg)
print(covImg)
print("Valeur propre : ", valp)
print("Vecteur propre : ", vecp)

print(img.shape)

plt.figure()
plt.axis("off")
plt.imshow(img)
plt.show()


#load.dataLoad()

