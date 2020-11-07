import dataLoad as load
import matplotlib.pyplot as plt
import matplotlib.axes as plot
import matplotlib.image as mpimg
import authentification
import numpy as np
import eigenFaces

load.dataLoad()

gallery = load.gallery
probes = load.probes
groundTruth = load.groundtruth

authentification.eigenAuth(probes[1],probes)

