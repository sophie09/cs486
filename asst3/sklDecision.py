from sklearn import tree

WORDCOUNT = 3566

def __processfile(dataname,total):
    docuArray = []
    for i in range(0, total):
        words = [0]*WORDCOUNT
        docuArray.append(words)

    with open(dataname) as d:
        for line in d:
            temp = line.split()
            index = int(temp[0])-1
            docuArray[index][int(temp[1])-1] = 1
    return docuArray

def __accuracy(treeResult,actual,total):
    falsePrediction = 0
    for i in range(total):
        if actual[i] != treeResult[i]:
            falsePrediction += 1
    acc = (total - falsePrediction) / total
    return acc

def main():
    TRAINDOCUMENTCOUNT = 1061
    TESTDOCUMENTCOUNT = 707
    depthList = list(range(1,20))
    trainData = __processfile("trainData.txt", TRAINDOCUMENTCOUNT)
    testData = __processfile("testData.txt", TESTDOCUMENTCOUNT)
    trainLabel = []
    testLabel = []

    with open("trainLabel.txt") as t1:
        for line in t1:
            trainLabel.append(int(line.split()[0]))

    with open("testLabel.txt") as t2:
        for line in t2:
            testLabel.append(int(line.split()[0]))


    for depth in depthList:
        clf = tree.DecisionTreeClassifier(criterion='entropy',max_depth=depth)
        clf = clf.fit(trainData, trainLabel)

        #training accuracy
        trainPrediction = clf.predict(trainData)
        trainAccuracy = __accuracy(trainPrediction,trainLabel,TRAINDOCUMENTCOUNT)

        #testing accuracy
        testPrediction = clf.predict(testData)
        testAccuracy = __accuracy(testPrediction,testLabel,TESTDOCUMENTCOUNT)

        print("Maximum depth = ", depth)
        print("training accuracy = ",trainAccuracy)
        print("testing accuracy = ",testAccuracy)

main()
