import csv
import math
import sys

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
Calculate Error
"""

def error(labels):
    maxLen = 0
    total = 0

    for i in labels:

        if(labels[i]>maxLen):
            maxLen = labels[i]

    for i in labels:
        total += labels[i]

    return 1-(maxLen/total)



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
            #print(label)
            if countRow != 1:
                if label in labels:
                    #print("label type:"+str(type(label)))  # label is string
                    labels[label] += 1
                else:
                    labels[label] = 1
    #print(labels[0]) #error
    #print(labels[1])

    #print(len(labels)) #2 = number of possible values of y

    #for i in labels:  #i is a string, it refer to all the keys in labels
        #print(labels[i])  #15 13 labels[i] is a


    entro = "entropy: "+str(entropy(labels))
    err = "error: "+str(error(labels))

    with open(sys.argv[2],"w") as output:
        output.write(entro+"\n")
        output.write(err)

    output.close()



if __name__ == "__main__":
    main()