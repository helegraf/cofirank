import os

for x in range(10):
    os.mkdir("out_N-10_seed-%d" % x)
    os.mkdir("out_N-20_seed-%d" % x)
    os.mkdir("out_N-50_seed-%d" % x)