import sys

def genConfigFor(N,seed):
    movielens = open("movielens.cfg")
    movielens_new = open("movielens_N-%s_seed-%d.cfg" % (N,seed),"w+")
    line = movielens.readline()

    while line:
        if line == "string cofi.outfolder out/\n":
            line = "string cofi.outfolder out_N-%s_seed-%d/\n" % (N,seed)
        elif line == "string cofibmrm.DtrainFile  data/data-u.data_N-10_seed-0_train.lsvm\n":
            line = "string cofibmrm.DtrainFile  data/data-u.data_N-%s_seed-%d_train.lsvm\n" % (N,seed)
        elif line == "string cofibmrm.DtestFile data/data-u.data_N-10_seed-0_test.lsvm\n":
            line = "string cofibmrm.DtestFile data/data-u.data_N-%s_seed-%d_test.lsvm\n" % (N,seed)

        movielens_new.write(line)
        line = movielens.readline()

    movielens.close()

for x in range(10):
    genConfigFor("10",x)
    genConfigFor("20",x)
    genConfigFor("50",x)