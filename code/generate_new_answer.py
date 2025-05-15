import json
import llm
import tqdm
import re
import random
import os
import argparse

LLM_path = "/home/llm_user/Baichuan2-13B-Chat"
folder = "./data"
file = "train_path.json"
sample_number = 0

def init_parser():
    global sample_number, folder, LLM_path
    parser = argparse.ArgumentParser(description='Knowledge-enhanced Q&A on large language models')
    parser.add_argument("-p", "--path", type=str, default="./data", help="The folder where the CMB data set or preprocessed files are located")
    parser.add_argument("-l", "--llm",type=str, default="/home/llm_user/Baichuan2-13B-Chat", help="The path where the local large language model is located")
    parser.add_argument("-n", "--number", type=int, default=0, help="Amount of knowledges provided for large language models")
    args = parser.parse_args()
    sample_number = args.number
    folder = args.path
    LLM_path = args.llm

def load_llm():
    print("Loading LLM {} ...".format(LLM_path))
    gpt = llm.BaiChuan_LLM(LLM_path)
    # print("Loading LLM {} ...".format("API"))
    # gpt = llm.api_LLM()
    print("Finish loading LLM!")
    return gpt

def exact_ans(res):
    res = res.upper()
    option = ["A", "B", "C", "D", "E", "F", "G"]
    opt = re.search(r"(答案|正确选项)(?:是|：|为|应该是|应该为)(.*?)(。|\.|$)", res, re.S)
    if opt:
        return "".join([x for x in option if x in str(opt)])
    return  "".join([i for i in option if i in res])


if __name__ == '__main__':

    init_parser()

    if not os.path.exists(os.path.join(folder, "result")):  #判断是否存在文件夹如果不存在则创建为文件夹
        os.makedirs(os.path.join(folder, "result"))

    gpt = load_llm()

    f = open(os.path.join(folder, file), "r")
    print("Reading " + file)
    data = json.load(f)
    
    cnt = 0
    query_template1 = "以下是中国{exam_type}中{exam_class}考试的一道{question_type}，\n{question}\n{option}\n，不需要做任何分析和解释，直接输出答案选项。同时我们给出了一些可能对得到答案有帮助的知识以供你参考{knowledge}"
    # query_template1 = "我们准备了一些知识:{path_sample}，请根据以上知识，不需要做任何分析和解释，直接输出下列问题答案的选项。问题如下：以下是中国{exam_type}中{exam_class}考试的一道{question_type}，\n{question}\n{option}\n。"
    query_template2 = "以下是中国{exam_type}中{exam_class}考试的一道{question_type}，不需要做任何分析和解释，直接输出答案选项。\n{question}\n{option}"

    for item in tqdm.tqdm(data):
        cnt += 1
        if cnt%50 == 0:
            del gpt
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


    json_str = json.dump(data, open(os.path.join(folder, "result/final_with_answer_{}.json".format(sample_number)), "w+"), indent=4, ensure_ascii=False)
