import math
from decisionNode import DecisionNode
from utilFunctions import processfile
from utilFunctions import accuracy

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


def infoGain(att, examples):
    p = 0  # examples in group 1
    p1 = 0  # examples in group 1 with attribute
    p2 = 0  # examples in group 1 without attribute
    n = 0  # examples in group 2
    n1 = 0  # examples in group 2 with attribute
    n2 = 0  # examples in group 2 without attribute
    for example in examples:
        if example[1] == 1:
            p += 1
            if example[0][att] == 1:
                p1 += 1
            else:
                p2 += 1
        else:
            n += 1
            if example[0][att] == 1:
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


def chooseAtt(attributes, examples):
    max = -1
    maxPos = -1
    for a in attributes:
        ig = infoGain(a, examples)
        if ig > max:
            max = ig
            maxPos = a
    return maxPos


def sameClass(examples):
    start = examples[0][1]
    for example in examples:
        if example[1] != start:
            return False
    return True


def modeClass(examples):
    p = 0  # examples in group 1
    n = 0  # examples in group 2
    for example in examples:
        if example[1] == 1:
            p += 1
        else:
            n += 1
    if p > n:
        return 1
    else:
        return 2


def splitExamples(examples, att):
    split_function = lambda examples: examples[0][att] == 1
    set1 = [row for row in examples if split_function(row)]
    set2 = [row for row in examples if not split_function(row)]
    return (set1, set2)


def DTL(examples, attributes, default, depth):
    # attributes start with zero!
    if not examples:
        return default
    elif sameClass(examples):
        return examples[0][1]
    elif (not attributes) or (depth == 0):
        return modeClass(examples)
    else:
        best = chooseAtt(attributes, examples)
        tree = DecisionNode(best)
        temp = splitExamples(examples, best)
        tExamples = temp[0]
        fExamples = temp[1]

        attributes.remove(best)
        mode = modeClass(examples)
        tSub = DTL(tExamples, attributes, mode, depth - 1)
        fSub = DTL(fExamples, attributes, mode, depth - 1)
        tree.tAdd(tSub)
        tree.fAdd(fSub)
        return tree


def predict(example, tree):
    if example[0][tree.word] == 1:
        if tree.tResult is not None:
            return tree.tResult
        else:
            return predict(example, tree.tb)
    else:
        if tree.fResult is not None:
            return tree.fResult
        else:
            return predict(example, tree.fb)


def printTree(tree, trainData,indent=''):
    print(indent + str(tree.word) + '? ')
    print(indent+'InfoGain =',infoGain(tree.word,trainData))
    if tree.tResult != None:
        print(indent + 'True->' + str(tree.tResult))
    else:
        print(indent + 'True->')
        printTree(tree.tb,trainData,indent + '  ')

    if tree.fResult != None:
        print(indent + 'False->' + str(tree.fResult))
    else:
        print(indent + 'False->')
        printTree(tree.fb,trainData,indent + '  ')


def main():
    TRAINDOCUMENTCOUNT = 1061
    TESTDOCUMENTCOUNT = 707
    WORDCOUNT = 3566

    trainData = processfile("trainData.txt", TRAINDOCUMENTCOUNT, WORDCOUNT,"trainLabel.txt")
    testData = processfile("testData.txt", TESTDOCUMENTCOUNT, WORDCOUNT, "testLabel.txt")

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
        trainAccuracy = accuracy(trainPrediction, trainData, TRAINDOCUMENTCOUNT)

        # testing accuracy
        for t in testData:
            testPrediction.append(predict(t, tree))
        testAccuracy = accuracy(testPrediction, testData, TESTDOCUMENTCOUNT)

        print("Maximum depth = ", depth)
        print("training accuracy = ", trainAccuracy)
        print("testing accuracy = ", testAccuracy)
    printTree(tree,trainData)


main()


