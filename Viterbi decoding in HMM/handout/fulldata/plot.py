import matplotlib.pyplot as plt

x = [10,100,1000,10000]
train =[0.832817,0.833686,0.860766,0.937865]
test = [0.832503,0.833554,0.856470,0.922569]

plt.plot(x, train,  label="TrainACC",color="red",linewidth=1)
plt.plot(x, test,  label="TestACC",color="black",linewidth=1)

plt.legend()
plt.xlabel('Sequences')
plt.ylabel('Accuracy')

plt.savefig("hw7.jpg")