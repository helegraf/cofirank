import statistics

def writeHeader(case_name, file):
    file.write("%s\n" % case_name)
    file.write("seed;N=10; N=20; n=50")

def get_result_from_file(result_file_name):
    return float(open(result_file_name).read().split(",")[-2])

def do_case(case_name):
    results_file = open("results_%s.csv" % case_name, "w+")

    results_10 = []
    results_20 = []
    results_50 = []

    for x in range(10):
        value1 = get_result_from_file("out_N-10_seed-%d/results.csv" % x)
        value2 = get_result_from_file("out_N-20_seed-%d/results.csv" % x)
        value3 = get_result_from_file("out_N-50_seed-%d/results.csv" % x)

        results_10.append(value1)
        results_20.append(value2)
        results_50.append(value3)

        results_file.write("%d;%f;%f;%f\n" % (x,value1,value2,value3))

    results_file.write("\n")
    results_file.write("mean;%f;%f;%f\n" % (statistics.mean(results_10),statistics.mean(results_20),statistics.mean(results_50)))
    results_file.write("std dev;%f;%f;%f\n" % (statistics.stdev(results_10),statistics.stdev(results_20)),statistics.stdev(results_50))
    
