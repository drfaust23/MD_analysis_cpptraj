#!/usr/bin/env python
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
dat = np.loadtxt('heavy_eps_2.0_cluster_cnumvtime.dat')
plt.plot(dat[:,0], dat[:,1], 'ro', ms=2.0, label='Cluster Index')
plt.xlabel('Frame')
plt.ylabel('Cluster Index')
plt.ylim(-2, 9)
plt.yticks(range(-1,9))
plt.savefig('heavy_eps_2.0_cluster_cnumvtime.png',format='png')
