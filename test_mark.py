import json
import load_data
import llm
import tqdm
import re
import Levenshtein

score = {}
folder = "./result_0320/"
res = []
res1 = []
correct_ans = set()
wrong_ans = set()
to_add = set()
def load_add():
    f = open("ex_add.txt","r")
    line = f.readline()
    while line:
        to_add.add(tuple(line.strip().split('\t')))
        line = f.readline()
    
    f = open("to_add.txt","r")
    line = f.readline()
    while line:
        wds = line.strip().split('\t')
        to_add.add((wds[0],wds[2],wds[1]))
        line = f.readline()

load_add()

for num in [0,3,1]:
    f = open(folder + "final_with_answer_{}.json".format(num), "r")
    data = json.load(f)
    for item in tqdm.tqdm(data):
        ans = item["answer"]
        ans1 = item["answer_with_triples"]
        paths = item["path_sample"]
        p = []
        for path in paths:
            if ((path[0][0][0][0]+".."+path[0][0][0][1],path[0][0][1][0]+".."+path[0][0][1][1],path[1][0]) in to_add):
            # print((path[0][0][0][0]+".."+path[0][0][0][1],path[0][0][1][0]+".."+path[0][0][1][1],path[1][0]))
                p.append((path[0][0][0][0]+".."+path[0][0][0][1],path[0][0][1][0]+".."+path[0][0][1][1],path[1][0]))
            if ((path[0][1][0][0]+".."+path[0][1][0][1],path[0][1][1][0]+".."+path[0][1][1][1],path[1][1]) in to_add):
                p.append((path[0][1][0][0]+".."+path[0][1][0][1],path[0][1][1][0]+".."+path[0][1][1][1],path[1][1]))
        item["triples"] = p
        score1 = (ans1 == ans)
        if num == 0 and ans1 != ans:
            correct_ans.add(item["question"])
        if num > 0 and ans1 == ans and item["question"] in correct_ans:
            # res.append({"question":item["question"], "option":item["option"]})
            res.append(item.copy())
            correct_ans.remove(item["question"])
        
        if num == 0 and ans1 == ans:
            wrong_ans.add(item["question"])
        if num > 0 and ans1 != ans and item["question"] in wrong_ans:
            # res.append({"question":item["question"], "option":item["option"]})
            res1.append(item.copy())
            wrong_ans.remove(item["question"])

        if item["exam_type"] not in score.keys():
            score[item["exam_type"]] = {}
        if item["exam_class"] not in score[item["exam_type"]].keys():
            score[item["exam_type"]][item["exam_class"]] = {}
        if "path_{}".format(num) not in score[item["exam_type"]][item["exam_class"]].keys():
            score[item["exam_type"]][item["exam_class"]]["path_{}".format(num)] = 0
        score[item["exam_type"]][item["exam_class"]]["path_{}".format(num)] += score1
        # score[item["exam_type"]][item["exam_class"]]["number"] += 1
            
json.dump(score, open(folder + "score.json", "w+"), indent=4, ensure_ascii=False)
json.dump(res, open(folder + "final_correct.json", "w+"), indent=4, ensure_ascii=False)
json.dump(res1, open(folder + "final_wrong.json", "w+"), indent=4, ensure_ascii=False)


# json.dump(out2, open("both_wrong.json", "w+"), indent=4, ensure_ascii=False)