import matplotlib.pyplot as plt

depth=[0,1,2,3,4,5,6,7]

trainErr = [ 0.4429530201342282, 0.20134228187919462,0.1342281879194631,0.11409395973154363,0.10738255033557047,0.087248322147651,0.0738255033557047,0.06711409395973154]

testErr = [0.28187919463087246,0.21686746987951808,0.1566265060240964,0.1686746987951807,0.20481927710843373,0.1686746987951807,0.1927710843373494,0.20481927710843373]



plt.plot(depth,trainErr,label="$training error$",color="red",linewidth=2)


plt.plot(depth,testErr,label="$testing error$",color="blue",linewidth=2)


plt.xlabel("Depth")

plt.ylabel("Error rate")

plt.legend()


plt.title("Error under Depth")

plt.savefig("pic.jpg")