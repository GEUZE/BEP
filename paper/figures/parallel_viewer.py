import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d

A = np.load('TEST_3_parallel-0.2-4844500-4845300-401.npy')
B = np.load('TEST_3_parallel(1)-0.2-4844500-4845300-401.npy')
C = np.load('TEST_3_parallel(2)-0.2-4844500-4845300-401.npy')
D = np.load('TEST_3_parallel(3)-0.2-4844500-4845300-401.npy')

plt.plot(A[0],A[1],B[0],B[1],C[0],C[1],D[0],D[1])