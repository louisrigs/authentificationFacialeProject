import dataLoad as load
import matplotlib.pyplot as plt
import matplotlib.axes as plot
import matplotlib.image as mpimg
import authentification as auth
import numpy as np

load.dataLoad(2)

gallery = load.gallery
probes = load.probes
probes1 = load.probes1
probes2 = load.probes2
groundTruth = load.groundtruth

print(auth.eigenAuth(probes[1],probes,1100000))

"""
	print(auth.eigenAuth(probes[1],probes,900000))
	print(auth.eigenAuth(probes[1],probes,800000))

	print(auth.bfAuth(probes1[10],probes2,1100000))
	print(auth.eigenAuth(probes1[10],probes2,350000))
	print(auth.eigenAuth(probes1[10],probes2,340000))
	print(auth.eigenAuth(probes1[10],probes2,335000))
	print(auth.eigenAuth(probes1[10],probes2,325000))

	print(auth.bfAuth(probes2[3],probes2,1100000))
	print(auth.eigenAuth(probes2[3],probes2,2000000))
	print(auth.eigenAuth(probes2[3],probes2,400000))
	print(auth.eigenAuth(probes2[3],probes2,300000))
	print(auth.eigenAuth(probes2[3],probes2,200000))

"""