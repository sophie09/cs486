import math
from decisionNode import DecisionNode

WORDCOUNT = 3566


def __processfile(dataname, total, labelname=None):
    docuArray = []
    for i in range(0, total):
        words = [0] * WORDCOUNT
        docuArray.append([i + 1, words])

    if labelname is not None:
        counter = 0
        with open(labelname) as l:
            for line in l:
                docuArray[counter].append(int(line.split()[0]))
                counter += 1

    with open(dataname) as d:
        for line in d:
            temp = line.split()
            index = int(temp[0]) - 1
            docuArray[index][1][int(temp[1]) - 1] = 1
    return docuArray


def __accuracy(treeResult, actual, total):
    falsePrediction = 0
    for i in range(total):
        if actual[i][2] != treeResult[i]:
            falsePrediction += 1
    acc = (total - falsePrediction) / total
    return acc


def entropy(a, b):
    if a == 0:
        tempa = 0
    else:
        tempa = math.log(a, 2)
    if b == 0:
        tempb = 0
    else:
        tempb = math.log(b, 2)
    return -a * tempa - b * tempb


def infoGain(att, docuArray):
    p = 0  # examples in group 1
    p1 = 0  # examples in group 1 with attribute
    p2 = 0  # examples in group 1 without attribute
    n = 0  # examples in group 2
    n1 = 0  # examples in group 2 with attribute
    n2 = 0  # examples in group 2 without attribute
    for d in docuArray:
        if d[2] == 1:
            p += 1
            if d[1][att] == 1:
                p1 += 1
            else:
                p2 += 1
        else:
            n += 1
            if d[1][att] == 1:
                n1 += 1
            else:
                n2 += 1

    if p1 + n1 == 0:
        truePorprotion1, falsePorprotion1 = 0, 0
    else:
        truePorprotion1 = p1 / (p1 + n1)
        falsePorprotion1 = n1 / (p1 + n1)
    if p2 + n2 == 0:
        truePorprotion2, falsePorprotion2 = 0, 0
    else:
        truePorprotion2 = p2 / (p2 + n2)
        falsePorprotion2 = n2 / (p2 + n2)

    remainder = (p1 + n1) / (p + n) * entropy(truePorprotion1, falsePorprotion1) + (p2 + n2) / (p + n) * entropy(
        truePorprotion2, falsePorprotion2)
    return (entropy(p / (p + n), n / (p + n)) - remainder)


def chooseAtt(attributes, docuArray):
    max = -1
    maxPos = -1
    for a in attributes:
        ig = infoGain(a, docuArray)
        if ig > max:
            max = ig
            maxPos = a
    return maxPos


def sameClass(docuArray):
    start = docuArray[0][2]
    for d in docuArray:
        if d[2] != start:
            return False
    return True


def modeClass(docuArray):
    p = 0  # examples in group 1
    n = 0  # examples in group 2
    for d in docuArray:
        if d[2] == 1:
            p += 1
        else:
            n += 1
    if p > n:
        return 1
    else:
        return 2


def splitExamples(rows, att):
    split_function = lambda row: row[1][att] == 1
    set1 = [row for row in rows if split_function(row)]
    set2 = [row for row in rows if not split_function(row)]
    return (set1, set2)


def DTL(docuArray, attributes, default, depth):
    # attributes start with zero!
    if not docuArray:
        return default
    elif sameClass(docuArray):
        return docuArray[0][2]
    elif (not attributes) or (depth == 0):
        return modeClass(docuArray)
    else:
        best = chooseAtt(attributes, docuArray)
        tree = DecisionNode(best)
        temp = splitExamples(docuArray, best)
        tExamples = temp[0]
        fExamples = temp[1]

        attributes.remove(best)
        mode = modeClass(docuArray)
        tSub = DTL(tExamples, attributes, mode, depth - 1)
        fSub = DTL(fExamples, attributes, mode, depth - 1)
        tree.tAdd(tSub)
        tree.fAdd(fSub)
        return tree


def predict(example, tree):
    if example[1][tree.word] == 1:
        if tree.tResult is not None:
            return tree.tResult
        else:
            return predict(example, tree.tb)
    else:
        if tree.fResult is not None:
            return tree.fResult
        else:
            return predict(example, tree.fb)


def printtree(tree, trainData,indent=''):
    print(indent + str(tree.word) + '? ')
    print(indent+'InfoGain =',infoGain(tree.word,trainData))
    # Is this a leaf node?

    if tree.tResult != None:
        print(indent + 'True->' + str(tree.tResult))
    else:
        print(indent + 'True->')
        printtree(tree.tb,trainData,indent + '  ')

    if tree.fResult != None:
        print(indent + 'False->' + str(tree.fResult))
    else:
        # Print the branches
        print(indent + 'False->')
        printtree(tree.fb,trainData,indent + '  ')

def main():
    TRAINDOCUMENTCOUNT = 1061
    TESTDOCUMENTCOUNT = 707
    trainData = __processfile("trainData.txt", TRAINDOCUMENTCOUNT, "trainLabel.txt")
    testData = __processfile("testData.txt", TESTDOCUMENTCOUNT, "testLabel.txt")

    depthList = list(range(4, 5))
    for depth in depthList:
        DEFAULT = 1
        attributes = list(range(WORDCOUNT))
        trainPrediction = []
        testPrediction = []

        tree = DTL(trainData, attributes, DEFAULT, depth)

        # training accuracy
        for d in trainData:
            trainPrediction.append(predict(d, tree))
        trainAccuracy = __accuracy(trainPrediction, trainData, TRAINDOCUMENTCOUNT)

        # testing accuracy
        for t in testData:
            testPrediction.append(predict(t, tree))
        testAccuracy = __accuracy(testPrediction, testData, TESTDOCUMENTCOUNT)

        print("Maximum depth = ", depth)
        print("training accuracy = ", trainAccuracy)
        print("testing accuracy = ", testAccuracy)

    printtree(tree,trainData)



main()
