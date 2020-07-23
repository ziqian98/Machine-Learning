import sys
import csv


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



def buildModelOneFormat(input, Vdict):
    labels = []

    allLinesDictList = []
    pack = []
    with open(input,"r") as tsvf:
        tsvAllLines = csv.reader(tsvf,delimiter = "\t")
        for oneline in tsvAllLines:
            #print(type(oneline[1].split()))
            labels.append(oneline[0])
            #print(oneline[0])
            oneLineWordList  =  oneline[1].split()
            oneLineLen = len(oneLineWordList)
            oneLineDict = {}
            for i in range (oneLineLen):
                #if (Vdict.has_key(oneLineWordList[i])):
                if oneLineWordList[i] in Vdict:
                    index = Vdict[oneLineWordList[i]]
                else:
                    continue
                if index in oneLineDict:
                    continue
                else:
                    oneLineDict[index] = 1
            allLinesDictList.append(oneLineDict)
                #print(oneLineWordList[i])
            #print("ddd")
            #break
    pack.append(labels)
    pack.append(allLinesDictList)
    return pack



def buildModelTwoFormat(input, Vdict):
    labels = []

    allLinesDictList = []
    pack = []
    with open(input,"r") as tsvf:
        tsvAllLines = csv.reader(tsvf,delimiter = "\t")
        for oneline in tsvAllLines:
            labels.append(oneline[0])
            oneLineWordList  =  oneline[1].split()
            oneLineLen = len(oneLineWordList)
            oneLineDict = {}
            for i in range (oneLineLen):
                #if (Vdict.has_key(oneLineWordList[i])):
                if oneLineWordList[i] in Vdict:
                    index = Vdict[oneLineWordList[i]]
                else:
                    continue
                if index in oneLineDict:
                    #continue
                    oneLineDict[index] = oneLineDict[index] +1
                else:
                    oneLineDict[index] = 1
            allLinesDictList.append(oneLineDict)
                #print(oneLineWordList[i])
            #print("ddd")
            #break

    length  = len(allLinesDictList)

    for i in range(0,length):
        copydict = allLinesDictList[i].copy()
        for (key,value) in copydict.items():
            if value > 3:
                allLinesDictList[i].pop(key)
            else:
                allLinesDictList[i][key] = 1


    pack.append(labels)
    pack.append(allLinesDictList)
    return pack




def writeModelFormat(output,labels,allLinesDictList):
    with open(output,"w") as outf:
        for i in range(0,len(allLinesDictList)):
            outf.write(labels[i]+"\t")
            oneLineDict = allLinesDictList[i]
            for (key,value) in oneLineDict.items():
                #print(type(key))
                #print(type(value)) # int
                outf.write(key+":"+str(value)+"\t")
            outf.write("\n")



def main():
    if sys.argv[8] == "2":
        print("222")
        Vdict  = build_Vdict(sys.argv[4])

        pack = buildModelTwoFormat(sys.argv[1], Vdict)
        writeModelFormat(sys.argv[5], pack[0], pack[1])

        pack = buildModelTwoFormat(sys.argv[2], Vdict)
        writeModelFormat(sys.argv[6], pack[0], pack[1])

        pack = buildModelTwoFormat(sys.argv[3], Vdict)
        writeModelFormat(sys.argv[7], pack[0], pack[1])

    else:
        print("111")
        Vdict = build_Vdict(sys.argv[4])

        pack = buildModelOneFormat(sys.argv[1], Vdict)
        writeModelFormat(sys.argv[5], pack[0], pack[1])

        pack = buildModelOneFormat(sys.argv[2], Vdict)
        writeModelFormat(sys.argv[6], pack[0], pack[1])

        pack = buildModelOneFormat(sys.argv[3], Vdict)
        writeModelFormat(sys.argv[7], pack[0], pack[1])


if __name__ == "__main__":
    main()
