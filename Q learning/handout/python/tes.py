import numpy as np
import math

a  = np.ones((3,2))
b= a.T
print(type(a[0][0]))
#print(a.shape)

print( np.random.randint(0,3) )

print(np.random.random())


print(math.log(8,2))

sum = 0

def h(p):
    return p*math.log(1/p,2)

print(h(0.6)+h(0.4))