import dataLoad as load
import matplotlib.pyplot as plt
import matplotlib.axes as plot
import matplotlib.image as mpimg
import numpy as np
import eigenFaces

load.dataLoad()


gallery = []
probes = []
groundTruth = []
valPropres, vecPropres, comp1, comp2 = eigenFaces.eigenFaces()


"""gallery = load.gallery"""
probes1 = load.probes1
"""
probes2 = load.probes2
groundTruth = load.groundtruth"""
