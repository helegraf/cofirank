import sys
import os.path
from statistics import mean
from statistics import stdev

def writeHeader(case_name, file):
    file.write("%s\n" % case_name)
    file.write("seed;N=10; N=20; n=50\n")

def get_result_from_file(result_file_name):
    if os.path.exists(result_file_name):
        file = open(result_file_name)
        num = float(file.read().split(",")[-3])
        file.close()
        return num
    else:
        return None

def do_case(case_name):
    results_file = open("results_%s.csv" % case_name, "w+")

    writeHeader(case_name,results_file)

    results_10 = []
    results_20 = []
    results_50 = []

    for x in range(10):
        value1 = get_result_from_file("out_N-10_seed-%d/result.csv" % x)
        value2 = get_result_from_file("out_N-20_seed-%d/result.csv" % x)
        value3 = get_result_from_file("out_N-50_seed-%d/result.csv" % x)

        results_file.write("%d" % x)

        if not (value1 == None):
            results_10.append(value1)
            results_file.write(";%f" % value1)
        else:
            results_file.write("; ")

        if not (value2 == None):
            results_20.append(value2)
            results_file.write(";%f" % value1)
        else:
            results_file.write("; ")

        if not (value3 == None):
            results_50.append(value3)
            results_file.write(";%f" % value1)
        else:
            results_file.write("; ")

        results_file.write("\n")

    results_file.write("\n")
    results_file.write("mean;%f;%f;%f\n" % (mean(results_10),mean(results_20),mean(results_50)))
    results_file.write("std dev;%f;%f;%f\n" % (stdev(results_10),stdev(results_20),stdev(results_50)))

    results_file.close()
 
do_case(sys.argv[1])