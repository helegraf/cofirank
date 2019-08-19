def append_to_file(file1,file2_name):
    file2 = open(file2_name)
    line = file2.readline()

    while line:
        file1.write(line)
        line = file2.readline()

    file2.close()

# open the 4 files and write them to a new file
file1 = open("combined_data_complete.txt","w+")

for x in range(1,5):
    print("Appending file {}".format(x))
    append_to_file(file1,"combined_data_{}.txt".format(x))

file1.close()