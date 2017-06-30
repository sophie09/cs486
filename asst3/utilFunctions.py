def processfile(dataname, total, wordcount, labelname=None):
    docuArray = []
    for i in range(0, total):
        words = [0] * wordcount
        docuArray.append([words])

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
            docuArray[index][0][int(temp[1]) - 1] = 1
    return docuArray


def accuracy(treeResult, actual, total):
    falsePrediction = 0
    for i in range(total):
        if actual[i][1] != treeResult[i]:
            falsePrediction += 1
    acc = (total - falsePrediction) / total
    return acc