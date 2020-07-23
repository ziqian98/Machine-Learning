import sys
import csv
import math
import numpy as np
import copy

errcount =0

class Node:
    def __init__ (self, left, right, depth, value, leftPathName):
        self.left = left
        self.right = right
        self.depth = depth
        self.value = value
        self.leftPathName = leftPathName  #if attribute value == leftname, it goes to left always



"""
Calculate Entropy
"""
def entropy(labels):
    if(len(labels)==1):  #only one type of label
        return 0
    total = 0
    for i in labels:
        total += labels[i]
    
    entropy = 0
    for i in labels:
        entropy += -(labels[i]/total)*math.log2(labels[i]/total)
    return entropy


"""
return q if all the y==1 in the data
"""
def ythesame(data):
    row = data.shape[0]
    data = data[1:row,:]  #remove the first column of attributes # 1: row returns 1 to (row-1)
    labelList = (data[:,-1]).tolist() #get the last column
    labels = {}
    for label in labelList:
        if label in labels:
            labels[label] +=1
        else:
            labels[label] = 1

    if len(labels) > 1:
        return 0
    else:
        return 1

"""
return sub dataset, x is the INDEX of attribute used to spit
"""
def getTwoSubdataset(x,dataset):
    sublist =[]
    subdatadata1 = dataset.copy()
    subdatadata2 = dataset.copy()

    x1 = dataset[1,x]

    flagx1 = 0
    while flagx1 == 0:
        for row in range(1,subdatadata1.shape[0]):
            if x1 != subdatadata1[row,x]:
                subdatadata1 = np.delete(subdatadata1,row,axis=0)  #atttirbutes equal to x1 are remained
                break
            if row == subdatadata1.shape[0]-1:
                flagx1 = 1

    flagx2 = 0
    while flagx2 ==0:
        for row in range(1,subdatadata2.shape[0]):
            if x1 == subdatadata2[row,x]:
                subdatadata2 = np.delete(subdatadata2,row,axis=0)
                break
            if row == subdatadata2.shape[0] - 1:
                flagx2 = 1



    subdatadata1 = np.delete(subdatadata1,x,axis=1)
    subdatadata2 = np.delete(subdatadata2, x, axis=1)

    sublist.append(subdatadata1)
    sublist.append(subdatadata2)

    return sublist



"""
Calculate I(Y;X)
"""
def mutalInfo(x,data): #x is the INDEX of column

    row = data.shape[0]
    data = data[1:row, :]  # remove the first row of attributes
    labelList = (data[:, -1]).tolist()  # get the last column
    labels = {}
    for label in labelList:
        if label in labels:
            labels[label] +=1
        else:
            labels[label] = 1

    hy = entropy(labels)

    attributeList = (data[:,x]).tolist()
    attrs = {}
    for att in attributeList:
        if att in attrs:
            attrs[att] +=1
        else:
            attrs[att] = 1

    if len(attrs) == 1:  #only one kind of attribute
        return 0;

    c = 0
    for att in attrs:  #att is key
        c += 1
        if c == 1:
            x1 = att
        if c == 2:
            x2 = att
    length  = attrs[x1] + attrs[x2]

    px1 = attrs[x1]/length
    px2 = 1-px1

    x1labels = {}
    x2labels = {}

    for row in range(length):
        if x1 == data[row,x] :  #may need to data[row,x].strip()
            if data[row,-1] in x1labels:
                x1labels[data[row,-1]] += 1
            else:
                x1labels[data[row,-1]] = 1
        else:
            if data [row,-1] in x2labels:
                x2labels[data[row, -1]] += 1
            else:
                x2labels[data[row, -1]] = 1


    hyx1 = entropy(x1labels)

    hyx2 = entropy(x2labels)

    I = hy - px1*hyx1 -px2*hyx2


    return I


"""
define leaf node
"""

def majorityVote(data):   #used to produce leaf
    global errcount
    row = data.shape[0]
    data = data[1:row,:]  #remove the first row of attributes # 1: row returns 1 to (row-1)
    labelList = (data[:,-1]).tolist() #get the last column

    labels = {}


    for label in labelList:
        if label in labels:
            labels[label] +=1
        else:
            labels[label] = 1

    maxLen = 0
    vote = ""

    for key in labels:
        if(labels[key]>maxLen):
            maxLen = labels[key]
            vote = key

    errcount =  errcount + (row-1) - maxLen

    return vote




"""
Build a tree
when to stop
1.reach max depth
2.all remaining labels are the same
3.depth == attribute number
"""

def tree(root,currentDepth,maxdepth,data):

    if(currentDepth == maxdepth+1): #leaf node
        datacopy = data.copy()
        nodeValue = majorityVote(datacopy)

        return Node(None, None, currentDepth, nodeValue,None)

    datacopy = data.copy()
    if ythesame(datacopy) == 1 :  #all the remaining labels are the same
        nodeValue = majorityVote(datacopy)

        return Node(None, None, currentDepth, nodeValue,None)

    datacopy = data.copy()
    if datacopy.shape[1] == 1:  #no attribute left
        nodeValue = majorityVote(datacopy)

        return Node(None, None, currentDepth, nodeValue,None)



    maxI = 0
    maxIPos = 0
    I = 0
    for x in range(0,data.shape[1]-1): #to exclude y
        datacopy = data.copy()
        I = mutalInfo(x, datacopy)
        if  I > maxI:
            maxI = I
            maxIPos = x

    if maxI == 0:
        datacopy = data.copy()
        nodeValue = majorityVote(datacopy)

        return  Node(None, None, currentDepth, nodeValue, None)

    if maxI > 0:
        nodeValue = data[0,maxIPos]
        leftWayName = data[1,maxIPos]
        root = Node(None , None, currentDepth, nodeValue, leftWayName)

        datacopy = data.copy()
        subdataList = getTwoSubdataset(maxIPos,datacopy)

        data0 = subdataList[0].copy()
        data1 = subdataList[1].copy()
        subdataList.clear()

        root.left = tree(root.left,currentDepth+1,maxdepth,data0)
        root.right = tree(root.right,currentDepth+1,maxdepth,data1)

        return root

    return root

"""
Identify what attributes are available
Selet an attribute that has max I
"""
def stump(data):

    numOFattr = data.shape[1]-1
    maxI = 0
    maxAttrPos = 0


    for i in range(numOFattr):

        datacopy = data.copy()


        MI = mutalInfo(i, datacopy)

        if MI>maxI:
            maxI = MI
            maxAttrPos = i

    nodeValue = data[0,maxAttrPos]
    leftWayName = data[1, maxAttrPos]
    root  =  Node(None, None, 1, nodeValue, leftWayName)
    return root

'''
Fisr entry is democrat number
'''
def countYNumber(data):

    numDemo = 0
    numRepub = 0

    numList = []

    labelList = data[1:data.shape[0],-1].tolist()  #skip first line
    for i  in labelList:
        if i == "democrat":
            numDemo +=1
        else:
            numRepub +=1

    numList.append(numDemo)
    numList.append(numRepub)
    return numList

'''
Print for debugging
'''
def preorder(root, data):
    if root.left:

        attrList = data[0,:].tolist()

        attrIndex = attrList.index(root.value)

        dataForSub = data.copy()

        subdataList = getTwoSubdataset(attrIndex, dataForSub)

        sub0 = subdataList[0].copy()
        sub1 = subdataList[1].copy()
        subdataList.clear()

        leftNumList = []
        rightNumList = []

        leftNumList = countYNumber(sub0)
        rightNumList = countYNumber(sub1)

        for i in range(0,root.depth):
            print("| ",end="")
        print(root.value,end="")
        if(root.leftPathName == "y"):
            print(" = y:",end="")
            print(" ["+str(leftNumList[0])+" democrat "+"/ "+str(leftNumList[1])+" republican]", end="")
        else:
            print(" = n:",end="")
            print(" [" + str(leftNumList[0]) + " democrat " + "/ " + str(leftNumList[1]) + " republican]",end="")
        print(" ")
        preorder(root.left,sub0)


        for i in range(0,root.depth):
            print("| ",end="")
        print(root.value, end="")
        if(root.leftPathName == "y"):
            print(" = n:",end="")
            print(" [" + str(rightNumList[0]) + " democrat " + "/ " + str(rightNumList[1]) + " republican]", end="")
        else:
            print(" = y:",end="")
            print(" [" + str(rightNumList[0]) + " democrat " + "/ " + str(rightNumList[1]) + " republican]", end="")
        print(" ")
        preorder(root.right,sub1)


'''
Used to predict the label a line of data
'''
def predictLabel(root, eachLine, attributeLine):

    while(root.left != None):
        pos = 0
        for attr in attributeLine:
            if root.value == attr:
                if root.leftPathName == eachLine[pos]:
                    root = root.left
                else:
                    root = root.right
            pos+=1


    return root.value


def main():

    labels = {}

    with open(sys.argv[1]) as tsvf:
        tsvLines = csv.reader(tsvf,delimiter = "\t")
        countRow = 0
        for oneLine in tsvLines:
            #print(type(oneLine))   #list
            #print(oneLine)
            #print(type(oneLine[-1]))  #string
            countRow += 1
            label = oneLine[-1]
            if countRow != 1:
                if label in labels:
                    #print("label type:"+str(type(label)))  # label is string
                    labels[label] += 1
                else:
                    labels[label] = 1

    numlist = []
    namelist =[]
    for i in labels:
        namelist.append(i)
        numlist.append(labels[i])
    print("[" + str(numlist[0])+" "+namelist[0]+" / " +str(numlist[1])+" "+namelist[1]+"]")

    rowcount = 0

    with open(sys.argv[1]) as tsvf:
        tsvLines = csv.reader(tsvf, delimiter='\t')
        for oneLine in tsvLines:
            rowcount += 1
            # npdata = np.vstack((npdata,np.array(oneLine)))
            if rowcount == 1:
                data = np.array(oneLine)
            else:
                data = np.vstack((data, oneLine))



    datacopy = data.copy()
    totalRow = data.shape[0]-1


    rootStump = stump(datacopy)
    firstOutPos = 0

    for i in range(0,data.shape[1]-1):
        if rootStump.value == data[0,i]:
            firstOutPos = i
            break


    datacopy = data.copy()


    subdataList = getTwoSubdataset(firstOutPos,datacopy)

    d0 = subdataList[0].copy()
    d1 = subdataList[1].copy()
    subdataList.clear()


    rootStump.left = tree(rootStump.left,2,int(sys.argv[3]),d0)

    rootStump.right = tree(rootStump.right,2,int(sys.argv[3]),d1)

    if sys.argv[1] == "politicians_train.tsv":
        datacopyForPrint = data.copy()
        preorder(rootStump,datacopyForPrint)


    errorRate = errcount/totalRow
    print("train error")
    print(errorRate)


    rowcount = 0

    with open(sys.argv[2]) as tsvf:
        tsvLines = csv.reader(tsvf, delimiter='\t')
        for oneLine in tsvLines:
            rowcount += 1

            if rowcount == 1:
                datanew = np.array(oneLine)

            else:
                datanew = np.vstack((datanew, oneLine))



    attributeLine = datanew[0,:].tolist()
    predictLabelList =[]
    for i in range(1,datanew.shape[0]):
        eachLine = datanew[i,:].tolist()
        predictL = predictLabel(rootStump,eachLine,attributeLine)
        predictLabelList.append(predictL)


    datatrain= data.copy()
    trainattributeLine = datatrain[0,:].tolist()
    trainpredictLabelList =[]
    for i in range(1,datatrain.shape[0]):
        traineachLine = datatrain[i,:].tolist()
        trainpredicL = predictLabel(rootStump,traineachLine,trainattributeLine)
        trainpredictLabelList.append(trainpredicL)


    with open(sys.argv[2]) as tsvf:
        tsvLines = csv.reader(tsvf,delimiter = "\t")
        testLabelList = []
        count = 0
        for oneLine in tsvLines:
            label = oneLine[-1]
            if count>0:  # skip first row
                testLabelList.append(label)
            count+=1


    e = 0
    for i in range(0,len(predictLabelList)):
        if predictLabelList[i] != testLabelList[i]:
            e+=1

    print("test error: ")
    testerror = e/len(predictLabelList)
    print(testerror)

    with open(sys.argv[4], "w") as output:
        for i in trainpredictLabelList:
            output.write(i + "\n")


    with open(sys.argv[5], "w") as output:
        for i in predictLabelList:
            output.write(i+"\n")

    with open(sys.argv[6], "w") as output:
        output.write("error(train): "+str(errorRate))
        output.write("\n")
        output.write("error(test): "+str(testerror))


def damn():
    labels = {}

    with open(sys.argv[1]) as tsvf:
        tsvLines = csv.reader(tsvf,delimiter = "\t")
        countRow = 0
        for oneLine in tsvLines:
            countRow += 1
            label = oneLine[-1]
            if countRow != 1:
                if label in labels:
                    labels[label] += 1
                else:
                    labels[label] = 1



    maxvote = ""
    maxvalue = 0
    lll = []
    for key in labels:
        if labels[key] > maxvalue:
            maxvalue = labels[key]
            maxvote = key
        lll.append(labels[key])

    trainTotal = 0
    for i in range(2):
        trainTotal += lll[i]

    trainErr = 1- maxvalue/trainTotal



#test condition

    countRow = 0
    tlabels= {}

    with open(sys.argv[2]) as tsvf:
        tsvLines = csv.reader(tsvf,delimiter = "\t")
        countRow = 0
        for oneLine in tsvLines:
            countRow += 1
            label = oneLine[-1]
            if countRow != 1:
                if label in tlabels:
                    tlabels[label] += 1
                else:
                    tlabels[label] = 1


    tmaxvote = ""
    tmaxvalue = 0
    tlll = []
    for key in tlabels:
        if tlabels[key] > tmaxvalue:
            tmaxvalue = tlabels[key]
            tmaxvote = key
        tlll.append(tlabels[key])

    testTotal = 0
    for i in range(2):
        testTotal += lll[i]

    testErr = 0
    if tmaxvote == maxvote:
        testErr = 1- tmaxvalue/testTotal

    else:
        testErr = tmaxvalue / testTotal

    with open(sys.argv[4], "w") as output:
        for i in range(trainTotal):
            output.write(maxvote + "\n")



    with open(sys.argv[5], "w") as output:
        for i in range(testTotal):
            output.write(maxvote+"\n")

    with open(sys.argv[6], "w") as output:
        output.write("error(train): "+str(trainErr))
        output.write("\n")
        output.write("error(test): "+str(testErr))


if __name__ == "__main__":
    if sys.argv[3] == "0":
        damn()
    else:
        main()