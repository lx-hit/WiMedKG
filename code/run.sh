#!/bin/bash
path=./data2
llm=/home/Disk/llm_models/Baichuan2-13B-Chat

python get_path.py --path ${path} --llm ${llm}

python generate_new_answer.py --path ${path} --llm ${llm} --number 3

python eval.py --path ${path}