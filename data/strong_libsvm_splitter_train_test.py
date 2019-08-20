import logging
import re

logging.basicConfig(format="[%(asctime)s] %(levelname)s\t%(message)s",
                    level=logging.DEBUG,
                    datefmt='%m/%d/%y %H:%M:%S')
logger = logging.getLogger( __name__ )

MIN_AMOUNT_REVIEWS = 50
TOP_K_USERS = 100
FILE = "u.data"

# read the whole data
logger.info("Rading data.")

usersWithValue = {}
movieamounts = {}
unimportant_movies = ""

file = open(FILE)
line = file.readline()

while line:

    parts = line.split("\t")[0:3]
    #print("Found parts: {}".format(parts))

    if (parts[0] in usersWithValue):
        usersWithValue[parts[0]].append(" " + parts[1] + ":" + parts[2])
    else:
        usersWithValue[parts[0]] = [" " + parts[1] + ":" + parts[2]]
    if (parts[1] in movieamounts):
        movieamounts[parts[1]] = movieamounts[parts[1]] + 1
    else:
        movieamounts[parts[1]] = 1
    
    line = file.readline()

#print("Found movies with amount ratings: {}".format(movieamounts))

# delete the movies with less than 50 reviews
logger.info("Locating sparsely reviewed movies.")

for movie in movieamounts.keys():
    if movieamounts[movie] < MIN_AMOUNT_REVIEWS:
        unimportant_movies += "|{}".format(movie)
unimportant_movies = unimportant_movies[1:]

#print("Found users {} before filtering by movie reviews".format(usersWithValue))
#print("Found unimportant movies {}".format(unimportant_movies))

logger.info("Discarding sparsely reviewed movies.")

r = re.compile(" ({}):.*".format(unimportant_movies))

def no_match(string):
    return not r.match(string)

#print("Discarding by regex {}".format(r))
for user in usersWithValue.keys():  
    usersWithValue[user] = list(filter(no_match,usersWithValue[user]))

#print("Found users {} after filtering by movie reviews.".format(usersWithValue))

# sort users by amount of reviewed movies
# < top 100 users are training
# top 100 users are testing

def custom_len(user):
    return -len(usersWithValue[user])  

logger.info("Locating 100 most active users and splitting data.")
x = 0
training_set = {}
testing_set = {}

for user in sorted(usersWithValue,key=custom_len):
    if len(usersWithValue[user]) > 0:
        if x < TOP_K_USERS:
            testing_set[user] = usersWithValue[user]
            #print("Adding user {} to testing set.".format(user))
        else:
            training_set[user] = usersWithValue[user]
            #print("Adding user {} to training set.".format(user))
    x += 1

# save -> the next step can be done with the created data
def customlen(elem):
    return int(elem.split(":")[0]) 

def writeDataset(values, data):
    dataset = open(data,"w+")

    for userRow in values.values():
        #print("ratings b4 sorting {}".format(userRow))
        ratings = sorted(userRow, key=customlen)
        #print("ratings after sorting {}".format(ratings))
        dataset.write("".join(userRow)[1:] + "\n")

    dataset.close()

writeDataset(training_set, "{}-train.lsvm".format(FILE))
writeDataset(testing_set, "{}-test.lsvm".format(FILE))