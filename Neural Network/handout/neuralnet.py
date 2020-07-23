import csv
import sys
import numpy as np
import math
import matplotlib.pyplot as plt


def getY(inpath):  #return a y lists
    y = []

    with open(inpath,"r") as input:
        lines = csv.reader(input)
        for eachline in lines:
            #print(type(eachline[0]))
            #print(type(eachline[0]))
            y.append(int(eachline[0]))
    yarr = np.array(y)
    #print("len of y: "+str(len(y)))
    yarr = yarr.reshape(len(y),1)
    #print("yarr: ")
    #print(yarr)
    input.close()
    return yarr

def getX(inpath):
    allLineList = []
    with open(inpath,"r") as input:
        lines = csv.reader(input)
        for eachLine in lines:
            x = eachLine[1:]
            #print("type x is")
            #print(type(x[0]))


            x = list(map(int,x))
            #print(type(x[0]))

            xarr = np.array(x)
            xarr = np.append(1,xarr)  # add bias
            allLineList.append(xarr)
    allLineArr = np.array(allLineList)
    input.close()
    return allLineArr




def randomInit(row,column):           #remember to set one column to zero outside
    return np.random.uniform(-0.1,0.1,(row,column))

def zeroInit(row, column):
    return np.zeros((row,column))

#input a vector, output a vector
def sigmoid(x):
    return 1.0/(1.0+math.exp(-x))

def sigmoidForward(a):
    size = a.shape[0]  # a is one column, each element has []
    #print("Hiddensize: " + str(a.shape[0]))
    z = []
    z.append(1)  #bias z0
    for i in range (0,size):
        z.append(sigmoid(a[i][0]))
    zarr = np.array(z)
    zarr = zarr.reshape(size+1,1)
    return zarr

def softmaxForward(b):
    #print("B is one column, has rows: "+ str(b.shape[0]))
    size  = b.shape[0]
    total = 0.0
    y=[]
    for i in range(0,size):
        total = total + math.exp(b[i][0])

    for i in range(0,size):
        y.append(math.exp(b[i][0])/total)

    yarr = np.array(y)
    yarr = yarr.reshape(size,1)  #yarr is one column
    return yarr

def crossEntropyForward(y,yhat):
    size = y.shape[0]
    #print("y.shape has rows: "+str(size))
    loss = 0.0
    for i in range (0,size):
        loss = loss + y[i][0] * math.log(yhat[i][0])
    loss = -loss

    return loss

def forwardProcedure(alpha,beta,input,output):  #input and output should be one column and each entry has []

    #a = np.matmul(alpha, input)
    #print(type(input[0][0]))
    #print(type(alpha[0][0]))
    a = np.matmul(alpha, input)  #4*129  *  129*1  = 4*1
    #print(alpha)
    #print("alpha")
    #print(alpha)


    #print("a is: ")
    #print(a)

    #print("a.shapea" + str(a.shape))

    z = sigmoidForward(a)  # z is one column, input is one column, each entry has []

    #print("z.shape" + str(z.shape))

    b = np.matmul(beta,z)  # b is one column

    yhat = softmaxForward(b)
    #print("yhat is: ")
    #print(yhat)

    j = crossEntropyForward(output, yhat)

    #print("entropy: " + str(j))

    return a,z,b,yhat,j

def softmaxBackward(y,yhat):
    size = y.shape[0]
    dlOVERdb = []
    for i in range(0,size):
        dlOVERdb.append(yhat[i][0]-y[i][0])

    totalRow = len (dlOVERdb)

    dlOVERdb_np = np.array(dlOVERdb)
    dlOVERdb_np = dlOVERdb_np.reshape(totalRow,1)

    return dlOVERdb_np

def sigmoidBackward(dlOverdz,z):    #input:dlOverdz is 4*1, z is 5*1
    size  = dlOverdz.shape[0]
    dlOverda = []

    for i in range (0,size):  #start from z[1][0], z[0][0] is bias
        dlOverda.append( dlOverdz[i][0] * z[i+1][0] * (1-z[i+1][0]) )

    dlOverdaArr = np.array(dlOverda)
    dlOverdaArr = dlOverdaArr.reshape(size,1)

    return dlOverdaArr




def backwardProcedure(beta,yhat,z,input,output):  # care x and y should be one column input, each entry has []

    dlOverdb = softmaxBackward(output,yhat)  # 3*1
    #print("dlOverdb: ")
    #print(dlOverdb)

    dlOverdbeta = np.matmul(dlOverdb,z.T)  #dlOverdbeta  #3*1 * 1*5  = 3*5

    betaStar = np.delete(beta,0,axis=1)  #betaStar  = 3 * 4, delete first column of beta

    dlOverdz = np.matmul(betaStar.T,dlOverdb)      #dlOverdz = 4*3  * 3*1 =  4*1  # bias Z0 is not included, here is not 5*1

    #print("z.shape")
    #print(z.shape)

    dlOverda = sigmoidBackward(dlOverdz,z)  #dlOverda 4*1   input:dlOverdz is 4*1, z is 5*1

    #print("dlOverda: ")
    #print(dlOverda)
    #print(dlOverda.shape)

    #kan = input.T
    #print(kan)
    #print(kan.shape)

    dlOverdalpha = np.matmul(dlOverda,input.T)  # input x is 7*1  dlOveralpha = 4*1  *  1*7

    return dlOverdalpha, dlOverdbeta


def sgd(alpha, beta, x, y, lr):   #x , y is one column
    a,z,b,yhat,j = forwardProcedure(alpha,beta,x,y)

    dlOverdalpha, dlOverdbeta = backwardProcedure(beta,yhat,z,x,y)

    alpha = alpha - lr * dlOverdalpha

    beta = beta - lr * dlOverdbeta

    return alpha,beta


def meanCrossEntropy(alpha,beta,trainX,trainY,lenY):
    totalEntropy = 0.0

    for i in range(0,lenY):
        posINy = trainY[i][0]
        x = trainX[i]
        x = x.reshape(len(x), 1)  # x is one column
        y = np.zeros(10)
        y[posINy] = 1
        y = y.reshape(10, 1)  # y is one column

        ji = forwardProcedure(alpha,beta,x,y)[-1]

        totalEntropy = totalEntropy + ji

    return totalEntropy/lenY


def predict(alpha,beta,xi,posINy):
    y = np.zeros(10)
    y[posINy] = 1
    y = y.reshape(10,1)
    xi = xi.reshape(len(xi),1)
    yhat = forwardProcedure(alpha,beta,xi,y)[-2]

    #print(yhat)
    max = 0.0
    maxpos = 0
    for i in range(0,10):
        if(max<yhat[i][0]):
            max = yhat[i][0]
            maxpos =i

    return maxpos

def calculateErr(truth, predict):  #truce is one column and each entry is [], predict is a list
    length = len(predict)

    errCount = 0
    for i in range(0,length):
        if(int(truth[i][0]) != int(predict[i])):
            errCount = errCount + 1

    return errCount/length

def main():
    trainY = getY(sys.argv[1])   # one column, each entry with []
    trainX = getX(sys.argv[1])  # multi row array


    testY = getY(sys.argv[2])
    testX = getX(sys.argv[2])

    lenY = trainY.shape[0]

    lenX = len(trainX[0])


    alpha = zeroInit(int(sys.argv[7]), lenX)
    beta = zeroInit(10, int(sys.argv[7]) + 1)


    if(int(sys.argv[8]) == 1): #random init
        #print("in random init")
        alpha = randomInit(int(sys.argv[7]),lenX)
        alpha[:,0] = 0.0  #bias column is set to zero
        beta = randomInit(10,int(sys.argv[7])+1)



    #print("alpha after init")
    #print(alpha)

    eppochList = []

    trainList = []

    testList = []
    with open(sys.argv[5],"w") as mOut:
        for epochNum in range(int(sys.argv[6])):
            for i in range(0,lenY):  # update alpha and beta on all data points
                posINy = trainY[i][0]
                x = trainX[i]
                x = x.reshape(len(x),1) # x is one column
                y = np.zeros(10)
                y[posINy] = 1
                y = y.reshape(10,1)  # y is one column
                alpha, beta = sgd(alpha, beta, x, y, float(sys.argv[9]))


            entropyTrainOneepoch = meanCrossEntropy(alpha,beta,trainX,trainY,lenY)

            entropyTestOneepoch = meanCrossEntropy(alpha,beta,testX,testY,testY.shape[0])


            trainList.append(entropyTrainOneepoch)

            testList.append(entropyTestOneepoch)

            eppochList.append(epochNum+1)

            print(len(eppochList))




            #print("epoch="+str(epochNum+1)+" "+"crossentropy(train): "+ str(entropyTrainOneepoch))

            mOut.write("epoch="+str(epochNum+1)+" "+"crossentropy(train): "+str(entropyTrainOneepoch)+"\n")
            mOut.write("epoch=" + str(epochNum + 1) + " " + "crossentropy(test): " + str(entropyTestOneepoch) + "\n")

        predictLabelsTrain = []

        predictLabelsTest = []

        for i in range(0,lenY):
            predictLabelsTrain.append(predict(alpha,beta,trainX[i],trainY[i][0]))

        for i in range(0,testY.shape[0]):
            predictLabelsTest.append(predict(alpha,beta,testX[i],testY[i][0]))

        #print(predictLabelsTest)

        trainErr = calculateErr(trainY,predictLabelsTrain)

        testErr = calculateErr(testY,predictLabelsTest)

        #print(trainErr)
        #print(testErr)

        mOut.write("error(train): "+str(trainErr))
        mOut.write("\n")
        mOut.write("error(test): "+str(testErr))

        mOut.close()

    with open(sys.argv[3],"w") as outTrain:
        length  = len(predictLabelsTrain)
        for i in range(0,length):
            outTrain.write(str(predictLabelsTrain[i]))
            outTrain.write("\n")
        outTrain.close()

    with open(sys.argv[4],"w") as outTest:
        length = len(predictLabelsTest)
        for i in range(0,length):
            outTest.write(str(predictLabelsTest[i]))
            outTest.write("\n")
        outTest.close()

    print(len(eppochList))

    # plt.plot(eppochList,trainList, label="$on train$", color="blue", linewidth=1)
    # plt.plot(eppochList,testList, label="$on test$", color="red", linewidth=1)
    #
    #
    # plt.xlabel("epoch")
    # plt.ylabel("average cross entropy")
    # plt.legend()
    # plt.title("lr = 0.001")
    # plt.savefig("lr0001.jpg")

if __name__ == "__main__":
    main()