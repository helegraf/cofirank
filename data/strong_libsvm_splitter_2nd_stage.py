import sys
import random

def customlen(elem):
    return int(elem.split(":")[0]) 

def create_data(file_name,N,seed):
    random.seed(seed)

    # read the test dataset
    f = open(file_name)
    ftrain = open("{}_strong_train.lsvm".format(file_name),"w+")
    ftest = open("{}_strong_test.lsvm".format(file_name),"w+")

    line = f.readline()

    while line:
        parts = line[:-1].split(" ")

        if len(parts) >= N + 10:
            # randomly put N=10 or N=20 or N=50 examples in the training, @least N+10 ratings have to be available for this
            train = sorted(random.sample(parts,N), key=customlen)
            train = [" {}".format(x) for x in train]
            ftrain.write("".join(train)[1:] + "\n")

            # put the rest in the testing
            test = sorted([x for x in parts if x not in train], key=customlen)
            test = [" {}".format(x) for x in test]
            ftest.write("".join(test)[1:] + "\n")

        line = f.readline()

    f.close()
    ftrain.close()
    ftest.close()

file_name = sys.argv[1]
N = int(sys.argv[2])
seed = int(sys.argv[3])

create_data(file_name,N,seed)