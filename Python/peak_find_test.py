#!/usr/bin/env python3

import sys
import random
import time
import numpy as np
import scipy.ndimage as ndimage
import scipy.ndimage.filters as filters
from scipy.signal import find_peaks
import matplotlib.pyplot as plt
#from skimage.feature import peak_local_max

nx = 1520
ny = 1000000
number = 16
neighbour = 4
threshold = 6

dm_pos = np.random.randint(low=0, high=nx, size=number)
ts_pos = np.random.randint(low=0, high=ny, size=number)
snr = np.random.randint(low=1, high=10, size=number)

print("dm: ", dm_pos)
print("ts: ", ts_pos)
print("snr: ", snr)

start = time.time()
a = np.zeros(shape=(nx,ny))
end = time.time()
print("Time to np.zeros: " + str(end - start))

median2 = np.median(dm_pos)
mean2 = np.mean(dm_pos)
std2 = np.std(dm_pos)
print(mean2,median2, std2)

for i in range(len(dm_pos)):
    ii = dm_pos[i]
    jj = ts_pos[i]
    a[ii][jj] += snr[i]

start = time.time()
data_max = filters.maximum_filter(a, neighbour)
maxima = (a == data_max)
del data_max
#data_min = filters.minimum_filter(a, neighbour)
#diff = ((data_max - data_min) > threshold)
#maxima[diff == 0] = 0
end = time.time()
print("Time to filter: " + str(end - start))

labeled, num_objects = ndimage.label(maxima)
print("Num objects: ", num_objects)
#coords = np.where(maxima)
print("label")
#slices = ndimage.find_objects(labeled)
#coords = ndimage.measurements.center_of_mass(a, labels=labeled, index=np.arange(1, num_objects + 1))
print("Done.")
#print(coords)
#x, y = [], []
#for dy,dx in slices:
#    x_center = (dx.start + dx.stop - 1)/2
#    x.append(x_center)
#    y_center = (dy.start + dy.stop - 1)/2
#    y.append(y_center)

#print(num_objects)
#print(np.amax(a,axis=0))
#plt.imshow(maxima)
#plt.colorbar()
#plt.savefig('data.png', bbox_inches = 'tight')

#peaks, _ = find_peaks(snr,height=0)
#plt.plot(snr)
#plt.plot(peaks, snr[peaks], "x")
#plt.show()

#np.savetxt("matrix-peak.csv", maxima, delimiter=" ")
#plt.plot(x,y,'ro')
#plt.savefig('test.png',bbox_inches= 'tight')

print("That's all folks.")

