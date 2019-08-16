import sys

N = sys.argv[1]
seed = sys.argv[2]

movielens = open("movielens.cfg")
movielens_new = open("movielens_N-%s_seed-%s.cfg" % (N,seed),"w+")
line = movielens.readline()

while line:
    if line == "string cofi.outfolder out/\n":
        line = "string cofi.outfolder out_N-%s_seed-%s/\n" % (N,seed)
    elif line == "string cofibmrm.DtrainFile  data/data-u.data_N-10_seed-0_train.lsvm\n":
        line = "string cofibmrm.DtrainFile  data/data-u.data_N-%s_seed-%s_train.lsvm\n" % (N,seed)
    elif line == "string cofibmrm.DtestFile data/data-u.data_N-10_seed-0_test.lsvm\n":
        line = "string cofibmrm.DtestFile data/data-u.data_N-%s_seed-%s_test.lsvm\n" % (N,seed)

    movielens_new.write(line)
    line = movielens.readline()

movielens.close()