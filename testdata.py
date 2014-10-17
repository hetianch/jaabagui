from numpy import genfromtxt
import numpy as np
my_data=genfromtxt('data.csv',delimiter=',')
a=my_data[np.nonzero(my_data==1)[0],:]
