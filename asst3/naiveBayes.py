import math
from utilFunctions import processfile
from utilFunctions import accuracy


def laplaceSmoothing(frequency,total):
    return (frequency+1)/(total+1)


def categoryTotal(data):
    # return total number of examples in class 1 and 2
    oneTotal = 0
    twoTotal = 0
    for d in data:
        if d[1] == 1:
            oneTotal += 1
        else:
            twoTotal += 1
    return [oneTotal,twoTotal]


def maxLikelihood(attribute,data,oneTotal,twoTotal):
    # return theta1 and theta2
    # theta1 = P(attribute = true|category = 1)
    # theta2 = P(attribute = true|category = 2)
    oneFrequency = 0
    twoFrequency = 0
    for d in data:
        if d[0][attribute] == 1:
            if d[1] == 1:
                oneFrequency += 1
            else:
                twoFrequency += 1
    oneFrequency = laplaceSmoothing(oneFrequency,oneTotal)
    twoFrequency = laplaceSmoothing(twoFrequency,twoTotal)
    return [oneFrequency,twoFrequency]


def predict(example,parameters,wordcount):
    oneParameters = list(map(lambda x:x[0],parameters))
    twoParameters = list(map(lambda x:x[1],parameters))
    onePostProb, twoPostProb = 0.5,0.5
    for word in range(wordcount):
        if example[0][word] == 1:
            onePostProb = onePostProb * oneParameters[word]
            twoPostProb = twoPostProb * twoParameters[word]
        else:
            onePostProb = onePostProb*(1-oneParameters[word])
            twoPostProb = twoPostProb*(1-twoParameters[word])
    if onePostProb > twoPostProb: return 1
    else: return 2


def main():
    TRAINDOCUMENTCOUNT = 1061
    TESTDOCUMENTCOUNT = 707
    WORDCOUNT = 3566

    trainData = processfile("trainData.txt", TRAINDOCUMENTCOUNT, WORDCOUNT, "trainLabel.txt")
    testData = processfile("testData.txt", TESTDOCUMENTCOUNT, WORDCOUNT, "testLabel.txt")

    totals = categoryTotal(trainData)
    mlset = []
    trainPrediction = []
    testPrediction = []

    words = range(WORDCOUNT)
    for word in words:
        mlset.append(maxLikelihood(word,trainData,totals[0],totals[1]))
    print(mlset)
    measurement = list(map(lambda x:abs(math.log(x[0])-math.log(x[1])),mlset))
    sortedDiscriminative = [w for (d, w) in sorted(zip(measurement, words),reverse=True)]
    print("Top ten discriminative words: ",sortedDiscriminative[:10])
    for s in sortedDiscriminative[:10]:
        print("Word: "+str(s)+", Measurement: "+str(measurement[s]))

    for t in trainData:
        trainPrediction.append(predict(t,mlset,WORDCOUNT))
    trainAccuracy = accuracy(trainPrediction, trainData, TRAINDOCUMENTCOUNT)

    for test in testData:
        testPrediction.append(predict(test,mlset,WORDCOUNT))
    testAccuracy = accuracy(testPrediction, testData, TESTDOCUMENTCOUNT)

    print("training accuracy = ", trainAccuracy)
    print("testing accuracy = ", testAccuracy)


main()










