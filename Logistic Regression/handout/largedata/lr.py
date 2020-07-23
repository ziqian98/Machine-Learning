import sys
import csv
import math
#import matplotlib.pyplot as plt

def build_Vdict (path):
    Vdict = {}
    oneline = []
    with open(path,"r") as f:
        for line in f:
           oneline = line.split(" ")
           #print (len(oneline))
           Vdict[oneline[0]] = str(oneline[1]).split("\n")[0]
    #print(type(Vdict["re-recorded"]))
    return Vdict

def getLabels(input):

    labels= []

    with open (input,"r") as tsvf:
        tsvAllLines = csv.reader(tsvf,delimiter="\t")
        for oneline in tsvAllLines:
            labels.append(oneline[0])

    return labels

def getIndexLists(input):
    allIndexLists = []

    with open(input,"r") as tsvf:
        tsvAllLines = csv.reader(tsvf,delimiter="\t")
        for oneline in tsvAllLines:
            oneLineIndexList = []
            length = len(oneline)
            for i in range(1,length):
                index = oneline[i].split(":")[0]
                #print(index)
                oneLineIndexList.append(index)
            allIndexLists.append(oneLineIndexList)
    #print(len(allIndexLists))
    return allIndexLists

def sgd(theta,x,y,lr):
    thetadotx = 0.0

    for i in range(0,len(x)):
        if x[i] != "":
            thetadotx = thetadotx + theta[int(x[i])]

    thetadotx = thetadotx + theta[-1]

    afterSig = 1/(1+math.exp(-thetadotx))

    #print(type(lr*(afterSig-y)))

    for i in range(0,len(x)):
        if x[i] != "":
            theta[int(x[i])] = theta[int(x[i])] - lr*(afterSig-y)

    theta[-1] = theta[-1] - lr*(afterSig-y)


    return theta

def predictAllSample(IndexLists,theta):

    labels = []
    for i in range(len(IndexLists)):
        thetadotx = 0.0
        for j in range(len(IndexLists[i])):
            if IndexLists[i][j] != "":
                thetadotx = thetadotx +theta[int(IndexLists[i][j])]

        thetadotx = thetadotx +theta[-1]

        afterSig = 1/(1+math.exp(-thetadotx))

        if(afterSig>0.5):
            labels.append(1)
        else:
            labels.append(0)
    return labels

def errorRate(PredicLabelList,actualLabelList):
    error = 0.0
    for i in range(len(actualLabelList)):
        if int(actualLabelList[i]) != int(PredicLabelList[i]):
            error+=1
    #print(error)
    return error/len(actualLabelList)

def getsum(theta):
    sum = 0.0
    for i in range(len(theta)):
        sum+=theta[i]
    return sum

def writeLabels(output,labels):
    with open(output,"w") as outf:
        for i in range(len(labels)):
            outf.write(str(labels[i])+"\n")

'''
def jtheta(theta,x,y):
    jt = 0.0
    for i in range(len(y)):
        thetadotxi = 0.0
        for j in range(len(x[i])):
            if x[i][j] != "":
                thetadotxi = thetadotxi + theta[int(x[i][j])]
        lg = math.log(1+math.exp(thetadotxi))
        forone = lg - thetadotxi * int(y[i])
        jt = jt+forone
    avgjt = jt/len(y)
    return avgjt
'''

def main():
    IndexListsTrain = getIndexLists(sys.argv[1])
    labelsTrain = getLabels(sys.argv[1])
    #print(len(labelsTrain))

    IndexListsVal = getIndexLists(sys.argv[2])
    labelsVal = getLabels(sys.argv[2])

    IndexListsTest = getIndexLists(sys.argv[3])
    labelsTest = getLabels(sys.argv[3])

    Vdict = build_Vdict(sys.argv[4])

    epoch = int(sys.argv[8])

    theta = []
    jthetaListVal = []
    jthetaLisTrain = []

    for i in range(len(Vdict)+1):
        theta.append(0.0)

    for i in range(epoch):
        for j in range (len(labelsTrain)):
            theta = sgd(theta,IndexListsTrain[j],int(labelsTrain[j]),0.1)
        #print(getsum(theta))
        print("epoch: "+str(i))

    #    jForOneVal = jtheta(theta,IndexListsVal,labelsVal)

    #    jForOneTrain = jtheta(theta,IndexListsTrain,labelsTrain)

    #    jthetaListVal.append(jForOneVal)
    #    jthetaLisTrain.append(jForOneTrain)

    #with open("valjModel2.txt","w") as valout:
    #    for i in range(len(jthetaListVal)):
    #        valout.write(str(jthetaListVal[i])+"\n")

    #with open("trainModel2.txt","w") as trainout:
    #    for i in range(len(jthetaLisTrain)):
    #        trainout.write(str(jthetaLisTrain[i])+"\n")

    #epochList = []
    #for i in range(epoch):
    #    epochList.append(i+1)

    #plt.plot(epochList,jthetaLisTrain, label="$train$", color="blue", linewidth=1)
    #plt.plot(epochList, jthetaListVal, label="$val$", color="red", linewidth=1)

    #plt.xlabel("epoch")

    #plt.ylabel("avg-neg-log-likelihood")

    #plt.legend()

    #plt.title("avg-neg-log-likelihood with epoch")

    #plt.savefig("model2.jpg")


    predictLabelsTrain = []
    predictLabelsTrain = predictAllSample(IndexListsTrain,theta)
    trainerr = errorRate(predictLabelsTrain,labelsTrain)

    predictLabelsTest = []
    predictLabelsTest = predictAllSample(IndexListsTest,theta)
    testerr = errorRate(predictLabelsTest,labelsTest)

    with open (sys.argv[7],"w") as errout:
        errout.write("error(train): "+str(trainerr))
        errout.write("\n")
        errout.write("error(test): " +str(testerr))


    writeLabels(sys.argv[5],predictLabelsTrain)
    writeLabels(sys.argv[6],predictLabelsTest)



if __name__ == "__main__":
    main()

