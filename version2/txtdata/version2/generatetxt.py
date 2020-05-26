import pickle
with open("./version2/snippet.pickle", "rb") as fr:
    qsl = pickle.load(fr)

ranks = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

def write_to_file(filename):
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

