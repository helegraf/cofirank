import random
import logging
import sys

logging.basicConfig(format="[%(asctime)s] %(levelname)s\t%(message)s",
                    level=logging.DEBUG,
                    datefmt='%m/%d/%y %H:%M:%S')
logger = logging.getLogger( __name__ )

def movielens(line,usersWithValue):
    parts = line.split("\t")[0:3]

    if (parts[0] in usersWithValue):
        usersWithValue[parts[0]].append(" " + parts[1] + ":" + parts[2])
    else:
        usersWithValue[parts[0]] = [" " + parts[1] + ":" + parts[2]]    

def netflix(line, usersWithValue):
    if line.endswith(':\n'):
        currmovie = line[:-2]
    elif not line == "\n":
        parts = line.split(',')

        if (parts[0] in usersWithValue):
            usersWithValue[parts[0]].append(" " + currmovie + ":" + parts[1])
        else:
            usersWithValue[parts[0]] = [" " + currmovie + ":" + parts[1]]

def read_dataset(addln, dataset):
    f = open(dataset)

    line = f.readline()
    usersWithValue = {}

    while line:      
        addln(line,usersWithValue)
        line = f.readline()
    
    f.close()

    return usersWithValue

def customlen(elem):
    return int(elem.split(":")[0]) 

def writeDataset(usersWithValue, traindataset, testdataset, seed, N):
    ftrain = open(traindataset,"w+")
    ftest = open(testdataset,"w+")

    random.seed(seed)

    for userRow in usersWithValue.values():
        if len(userRow) >= N + 10:
            # write N random train entries
            train = sorted(random.sample(userRow,N), key=customlen)
            ftrain.write("".join(train)[1:] + "\n")

            # write the rest as test entries
            test = sorted([x for x in userRow if x not in train], key=customlen)
            ftest.write("".join(test)[1:] + "\n")

    ftrain.close()
    ftest.close()

def convertDataset(dataset, conversionmethod, N, seed):
    logger.info("Starting first pass (matching movie ids and ratings with users)")

    usersWithValue = read_dataset(conversionmethod, dataset)

    logger.info("First pass done.")
    logger.info("Starting second pass (Sorting movie ratings for users + file writing).")

    writeDataset(usersWithValue,"data-%s_N-%d_seed-%d_train.lsvm" % (dataset,N,seed),"data-%s_N-%d_seed-%d_test.lsvm" % (dataset,N,seed), seed, N)

    logger.info("Second pass done.")

data = sys.argv[1]
if sys.argv[2]=='movielens':
    method = movielens
else:
    method = netflix
N = int(sys.argv[3])
seed = int(sys.argv[4])
convertDataset(data, method, N, seed)