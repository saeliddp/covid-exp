import pickle
import random

with open("./version2/snippet.pickle", "rb") as fr:
    qsl = pickle.load(fr)

#fake news ranks = 90, 91

def original_results(filename):
    ranks = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    fw = open("./version2/txtdata/version2/" + filename, "w")
    curr_q = 1
    for qs in qsl:
        cr = 1
        for rank in ranks:
            line = str(curr_q) + "X" + " Q0 " + str(curr_q) + "00" + str(rank) + " " + str(cr) + " X g\n"
            cr += 1
            fw.write(line)
        curr_q += 1
    fw.close()
    
def altered_results(filename):
    fw = open("./version2/txtdata/version2/" + filename, "w")
    curr_q = 1
    for qs in qsl:
        ranks = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        if curr_q <= 10:
            ranks[random.randint(0, 4)] = 90
            ranks[random.randint(5, 9)] = 91
        else:
            ranks[random.randint(0, 4)] = 90
        cr = 1
        for rank in ranks:
            line = str(curr_q) + "X" + " Q0 " + str(curr_q) + "00" + str(rank) + " " + str(cr) + " X g\n"
            cr += 1
            fw.write(line)
        curr_q += 1
    fw.close()

