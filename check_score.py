import json
# f = open("./base/score.json", "r")
# f = open("./one_first/score.json", "r")
# f = open("./swap/score.json", "r")
# f = open("./data_2/score.json", "r")
folder = "./result_0311/"
f = open(folder + "score.json", "r")
lt = ["path_1", "path_3", "path_5", "path_7", "path_9", "path_10"]
data = json.load(f)
for i in data.keys():
    for j in data[i].keys():
        for k in lt:
            if int(data[i][j][k]) > int(data[i][j]["path_0"]):
                print(i, j, k[5:]+"条", data[i][j]["path_0"], data[i][j][k], " up", "{:.2f}%".format((data[i][j][k]/data[i][j]["path_0"] - 1)*100))
            # else:
                # print(data[i][j]["path_0"], data[i][j][k], " down", "{:.2f}%".format((1 - data[i][j][k]/data[i][j]["path_0"])*100))