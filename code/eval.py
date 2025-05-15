import json
import argparse
import os

def init_parser():
    global data_path, knowledges_number
    parser = argparse.ArgumentParser(description='Evaluate answer score')
    parser.add_argument("-p", "--path", type=str, default="./data", help="The folder where the CMB data set or preprocessed files are located")
    args = parser.parse_args()
    data_path = args.path

if __name__ == '__main__':
    init_parser()
    data_path = os.path.join(data_path, "result")
    files = [f for f in os.listdir(data_path)]
    score = {}
    type_num = {}
    for file in files:
        if not file.endswith(".json"):
            continue
        if not file.startswith("final_with_answer_"):
            continue
        num = int(file.split("_")[-1].split(".")[0])   
        f = open(os.path.join(data_path, file), "r")
        data = json.load(f)
        if file not in score.keys():
            score[file] = 0
        
        for item in data:
            ans = item["answer"]
            ans1 = item["answer_with_triples"]
            score1 = (ans1 == ans)
            score[file] += score1

    # f = open(os.path.join(data_path, "result.txt"), "w+")
    for file, score_value in score.items():
        print("{} {} correct\n".format(file, score_value))