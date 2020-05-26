with open("results.txt", "r") as fr:
    lines = fr.readlines()
    

fw = open("topten_results.txt", "w")
curr_rank = 0
for line in lines:
    if "Query" in line:
        curr_rank = 0
    else:
        if "Rank=" in line:
            curr_rank += 1
    
    if curr_rank <= 10:
        fw.write(line)

fw.close()