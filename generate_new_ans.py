import json
import llm
import tqdm
import re
import sys
import random
import os

LLM_path = "/home/llm_user/Baichuan2-13B-Chat"
folder = "./result_0320/"
file = "train_path.json"

def load_llm():
    print("Loading LLM {} ...".format(LLM_path))
    gpt = llm.BaiChuan_LLM()
    gpt.init_LLM(LLM_path)
    print("Finish loading LLM!")
    return gpt

sample_number = int(sys.argv[1])

def exact_ans(res):
    res = res.upper()
    option = ["A", "B", "C", "D", "E", "F", "G"]
    opt = re.search(r"(答案|正确选项)(?:是|：|为|应该是|应该为)(.*?)(。|\.|$)", res, re.S)
    if opt:
        return "".join([x for x in option if x in str(opt)])
    return  "".join([i for i in option if i in res])


if __name__ == '__main__':

    if not os.path.exists(folder):  #判断是否存在文件夹如果不存在则创建为文件夹
        os.makedirs(folder)

    gpt = load_llm()

    f = open(folder + file, "r")
    print("Reading " + file)
    data = json.load(f)
    
    cnt = 0
    query_template1 = "以下是中国{exam_type}中{exam_class}考试的一道{question_type}，\n{question}\n{option}\n，不需要做任何分析和解释，直接输出答案选项。同时我们给出了一些可能对得到答案有帮助的知识以供你参考{knowledge}"
    # query_template1 = "我们准备了一些知识:{path_sample}，请根据以上知识，不需要做任何分析和解释，直接输出下列问题答案的选项。问题如下：以下是中国{exam_type}中{exam_class}考试的一道{question_type}，\n{question}\n{option}\n。"
    query_template2 = "以下是中国{exam_type}中{exam_class}考试的一道{question_type}，不需要做任何分析和解释，直接输出答案选项。\n{question}\n{option}"

    for item in tqdm.tqdm(data):
        cnt += 1
        if cnt%50 == 0:
            gpt = load_llm()
        
        path = item["paths"]

        if len(path) < sample_number:
            item["path_sample"] = path
        else :
            item["path_sample"] = random.sample(path, sample_number)            

        item["knowledge"] = ""
        for path in item["path_sample"]:
            item["knowledge"] += ","+path[2]

        if len(item["path_sample"]) > 0:
            item["query"] = query_template1.format_map(item)
        else:
            item["query"] = query_template2.format_map(item)

        item["response"] = gpt.query(item["query"])
        item["answer_with_triples"] = exact_ans(item["response"])


    json_str = json.dump(data, open(folder+"/final_with_answer_{}.json".format(sample_number), "w+"), indent=4, ensure_ascii=False)
