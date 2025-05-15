import json
import load_data
import tqdm
import llm
import random
import argparse
import os

data_path = "./data/"
LLM_path = "/home/Disk/llm_models/Baichuan2-13B-Chat"

def init_parser():
    global data_path, LLM_path
    parser = argparse.ArgumentParser(description='Retrieve problem-related knowledge from the knowledge graph')
    parser.add_argument("-p", "--path", type=str, default="./data", help="The folder where the CM3B data set or preprocessed files are located")
    parser.add_argument("-l", "--llm",type=str, default="/home/Disk/llm_models/Baichuan2-13B-Chat", help="The path where the local large language model is located")
    args = parser.parse_args()
    data_path = args.path
    LLM_path = args.llm

def has_number(string):
    for char in string:
        if char.isdigit():
            return True
    return False

def get_entity_from_text(text):
    ents = set()
    for e in entity:
        if e[0] in text:
            ents.add(e)
    return ents

# subtriples = set()
# subentity = set()

def get_path_1(ent1, ent2):
    ret = []
    if ent1 in triples_head_tail.keys() and ent2 in triples_head_tail[ent1].keys():
        ret.append((((ent1, ent2), (ent1, ent2)), (triples_head_tail[ent1][ent2], triples_head_tail[ent1][ent2]), rel_map[triples_head_tail[ent1][ent2]].format_map({"head": ent1[0], "tail": ent2[0]})))
        # subtriples.add((ent1, ent2, triples_head_tail[ent1][ent2]))
        # subentity.add(ent1)
        # subentity.add(ent2)
    if ent2 in triples_head_tail.keys() and ent1 in triples_head_tail[ent2].keys():
        ret.append((((ent2, ent1), (ent2, ent1)), (triples_head_tail[ent2][ent1], triples_head_tail[ent2][ent1]), rel_map[triples_head_tail[ent2][ent1]].format_map({"head": ent2[0], "tail": ent1[0]})))
        # subtriples.add((ent2, ent1, triples_head_tail[ent2][ent1]))
        # subentity.add(ent1)
        # subentity.add(ent2)

    return ret

def get_path_2(ent1, ent2):
    mp = {}
    t1 = set()
    t2 = set()
    # print( "----------------- t1 ------------------ ")
    if ent1 in triples_head_tail.keys():
        for tail in triples_head_tail[ent1].keys():
            t1.add(tail)
    # print( "----------------- t2 ------------------ ")
    if ent2 in triples_tail_head.keys():
        for head in triples_tail_head[ent2].keys():
            t2.add(head)
    t1 = t1.intersection(t2)
    # print(" ----------------- inc ------------------ ")
    ret = []
    rel = []
    for i in t1:
        mp[(triples_head_tail[ent1][i], triples_head_tail[i][ent2])] = ((ent1, i),(i, ent2))
        # subtriples.add((ent1, i, triples_head_tail[ent1][i]))
        # subtriples.add((i, ent2, triples_head_tail[i][ent2]))
        # subentity.add(ent1)
        # subentity.add(i)
        # subentity.add(ent2)
    for t in mp.keys():
        wd = rel_map[t[0]].format_map({"head": mp[t][0][0][0], "tail": mp[t][0][1][0]}) + "并且" + rel_map[t[1]].format_map({"head": mp[t][1][0][0], "tail": mp[t][1][1][0]})
        ret.append((mp[t], t, wd))
    return ret

if __name__ == "__main__":
    init_parser()
    print("Loading KG...")
    # triples:根据关系查找三元组
    # triples_head:根据关系和头实体查找三元组
    # triples_tail：根据关系和尾实体查找三元组
    # triples_head_tail：根据头实体和尾实体查找三元组
    # triples_tail_head：根据尾实体和头实体查找三元组
    out = []
    # 读取知识图谱
    triples, triples_head, triples_tail,triples_head_tail, triples_tail_head = load_data.load_triples(os.path.join(data_path,"triple.txt"))
    entity = load_data.load_entity(os.path.join(data_path,"entity.txt"))
    print("Finish loading KG...")

    print("Loading LLM {} ...".format(LLM_path))
    gpt = llm.BaiChuan_LLM(LLM_path)
    # print("Loading LLM {} ...".format("API"))
    # gpt = llm.api_LLM()
    print("Finish loading LLM!")

    f = open(os.path.join(data_path, "train.json"), "r")
    data = json.load(f)
    # 将三元组映射为自然语言的映射文件
    f = open(os.path.join(data_path,"relation_map.json"), "r")
    rel_map = json.load(f)
    # typelist = ["初级中药士", "初级中药师", "医技士", "主管技师", "临床医学", "考研政治", "西医综合", "基础医学"]
    typelist = ["执业医师", "中级职称", "高级职称", "执业西药师", "初级药士", "初级药师", "主管药师", "医技士", "医技师", "主管技师", "基础医学", "临床医学", "西医综合"]

    # 主要是这里
    # random.shuffle(data)
    cnt = 0

    for item in tqdm.tqdm(data):
        if item["exam_class"] not in typelist:
            continue
        flag = False
        for opt in item["option"].keys():
            if not has_number(item["option"][opt]):
                flag = True
        if not flag:
            continue
        to_del = set()
        ents = get_entity_from_text(item["question"]) # 匹配问题中的实体
        # 若匹配到的A包含B，那么删除B
        for a in ents:
            for b in ents:
                if a[0] != b[0] and a[0] in b[0]:
                    to_del.add(a)
                    break
        ents = ents - to_del
        item["question_entities"] = list(ents)

        to_del = set()
        # 同上，匹配选项中的实体
        ents1 = get_entity_from_text(str(item["option"]))
        for a in ents1:
            for b in ents1:
                if a[0] != b[0] and a[0] in b[0]:
                    to_del.add(a)
                    break
        ents1 = ents1 - to_del - ents
        item["option_entities"] = list(ents1)

        paths = []
        for ent1 in item["question_entities"]:
            for ent2 in item["option_entities"]:
                # 获取二跳路径
                paths.extend(get_path_2(tuple(ent1), tuple(ent2)))
                paths.extend(get_path_2(tuple(ent2), tuple(ent1)))
                # 获取一跳路径
                paths.extend(get_path_1(tuple(ent1), tuple(ent2)))
        if len(paths) == 0:
            continue
        rel_set = set()
        for path in paths:
            for tp in path[1]:
                rel_set.add(tp)
        item["relations"] = list(rel_set)

        # 上边就把实体和路径提出来了，只支持一跳两跳

        if len(rel_set) > 3:
            cnt += 1
            # print(cnt)
            if cnt%50 == 0:
                del gpt
                print("Loading LLM {} ...".format(LLM_path))
                gpt = llm.BaiChuan_LLM(LLM_path)
                print("Finish loading LLM!")
            problem = "以下是中国{exam_type}中{exam_class}考试的一道{question_type}，\n{question}\n{option}。问题结束。现在给出一些实体关系，请按照对这道题目求解从有帮助到无帮助的的顺序将给出的实体关系排序，并直接按照输入的格式输出最优的前三个实体关系即可，无需输出任何分析。给出的实体关系如下{relations}".format_map(item)
            # problem = "以下是中国{exam_type}中{exam_class}考试的一道{question_type}，\n{question}\n{option}。问题结束。现在给出一些实体关系，请根据这道题目的内容，给出最有助于解决该问题的实体关系，并按照输入时的格式输出，无需输出任何分析。给出的实体关系如下{relations}".format_map(item)
            res = gpt.query(problem)
            rk = []
            for rel in rel_set:
                wds = rel.split("\\")
                rel1 = wds[0] + "\\\\" + wds[1] + "\\\\" + wds[2]
                rel2 = wds[0] + wds[1] + wds[2]
                p1 = res.find(rel)
                p2 = res.find(rel1)
                p3 = res.find(rel2)
                if p1 == -1 and p2 == -1 and p3 == -1:
                    continue
                rk.append((rel, max(max(p1, p2), p3)))
            rk.sort(key = lambda x:x[1])
            rk = rk[:3]
            true_relations = []
            for tp in rk:
                true_relations.append(tp[0])
        else:
            true_relations = list(rel_set)
        item["relations"] = true_relations
        
        rel_path = []
        for path in paths:
            if path[1][0] in item["relations"] or path[1][1] in item["relations"]:
                rel_path.append(path)
        item["paths"] = rel_path
        
        if rel_path:
            out.append(item.copy())

    json.dump(out, open(os.path.join(data_path, "train_path.json"), "w+"), indent=4, ensure_ascii=False)
    # subtriples = list(subtriples)
    # subtriples.sort(key=lambda x: (x[0][0], x[1][0], x[2]))
    # subentity = list(subentity)
    # subentity.sort(key=lambda x: (x[0], x[1]))
    
    # with open(os.path.join(data_path, "sub_triples.txt"), "w+") as f:
    #     for i in subtriples:
    #         f.write("{}\t{}\t{}\n".format(i[0][0]+".."+i[0][1], i[1][0] + ".." + i[1][1], i[2]))
    # with open(os.path.join(data_path, "sub_entity.txt"), "w+") as f:
    #     for idx,i in enumerate(subentity):
    #         f.write("{}..{}\t{}\n".format(i[0],i[1],idx))