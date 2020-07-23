import sys


def createIndexDic(path):
    i=0
    dic = {}

    with open(path,"r")as readline:
        for eachLine in readline:
            eachLine = eachLine.strip("\n")
            dic[eachLine] = i
            i=i+1

    return dic

def getTrainList(path):
    trainList = []

    count = 0

    with open(path,"r") as readline:
        for eachLine in readline:

            count  = count+1
            if(count == 10001):
                break;
            print(count)

            eachLine = eachLine.strip("\n")
            entriesInOneline = eachLine.split(" ")


            oneLineList = []

            for entry in entriesInOneline:
                pair = [] #word tag

                pair.append(entry.split("_")[0])
                pair.append(entry.split("_")[1])

                oneLineList.append(pair)

            trainList.append(oneLineList)

    return trainList

def buildA(tagDic,trainList):
    a = []
    for i in range(len(tagDic)):
        temp = []
        for j in range(len(tagDic)):
            temp.append(0.0)
        a.append(temp)


    for i in range (len(trainList)):
        for j in range(len(trainList[i])-1):
            former = trainList[i][j]
            latter = trainList[i][j+1]
            #print(former)

            row = tagDic[former[1]]
            col = tagDic[latter[1]]

            a[row][col] = a[row][col] + 1.0

    return smoothANDnorm(a)

def buildB(tagDic, wordDic, trainList):
    b = []
    for i in range(len(tagDic)):
        temp = []
        for j in range(len(wordDic)):
            temp.append(0.0)
        b.append(temp)

    for i in range (len(trainList)):
        for j in range (len(trainList[i])):
            row = tagDic[trainList[i][j][1]]
            col = wordDic[trainList[i][j][0]]

            b[row][col] = b[row][col] + 1.0

    return smoothANDnorm(b)




def prior(tagDic, trainList):
    c = []
    for i in range(len(tagDic)):
        c.append(0.0)

    for i in range(len(trainList)):
        row = tagDic[trainList[i][0][1]]

        c[row] =  c[row] + 1.0

    return smoothANDnormForPrior(c)



def smoothANDnormForPrior(matrix):
    sum = 0.0

    for i in range (len(matrix)):
        matrix[i]  = matrix[i] + 1
        sum = sum + matrix[i]

    for i in range(len(matrix)):
        matrix[i] = matrix[i] / sum

    return matrix


def smoothANDnorm(matrix):


    sum = [0.0] * len(matrix)

    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            matrix[i][j] = matrix[i][j] + 1.0
            sum[i] = sum[i] + matrix[i][j]

    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            matrix[i][j] = matrix[i][j] / sum[i]

    return matrix

def writePrior(path, matrix):
    with open(path, "w") as out:
        for entry in matrix:
            out.write(str(entry))
            out.write("\n")



def writeAB(path, matrix):
    with open(path, "w") as out:
        for row in range(len(matrix)):
            for col in range(len(matrix[row])):
                out.write(str(matrix[row][col]))
                if col == len(matrix[row]) -1:
                    out.write("\n")
                else:
                    out.write(" ")

def main():
    wordDic = createIndexDic(sys.argv[2])
    #print(wordDic)
    tagDic = createIndexDic(sys.argv[3])
    #print(tagDic)

    trainList = getTrainList(sys.argv[1])

    A = buildA(tagDic,trainList)

    B = buildB(tagDic,wordDic,trainList)

    C = prior(tagDic,trainList)


    writePrior(sys.argv[4],C)
    writeAB(sys.argv[5],B)
    writeAB(sys.argv[6],A)
    #
    #
    # print(trainList)
    # print(trainList[0][1][1])

if __name__ == "__main__":
    main()