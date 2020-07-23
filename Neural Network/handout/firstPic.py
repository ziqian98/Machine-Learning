import matplotlib.pyplot as plt

eppochList = [5,20,50,100,200]
trainList = [0.5372,0.1339,0.05315,0.04665,0.0469]
testList = [0.6710,0.5549,0.46712,0.4343,0.4216]



plt.plot(eppochList,trainList, label="$train$", color="blue", linewidth=1)
plt.plot(eppochList,testList, label="$test$", color="red", linewidth=1)


plt.xlabel("number of hidden units")
plt.ylabel("average cross entropy")
plt.legend()
plt.savefig("firstPicNew.jpg")