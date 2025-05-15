- [get_path.py](./get_path.py): 在知识图谱中获取问题相关的一跳、二跳路径。
- [generate_new_answer.py](./generate_new_answer.py): 在识别出的路径中均匀抽取一定数量的路径知识，加入到prompt中，辅助大模型得出答案。  
- [eval.py](./eval.py): 为得到的答案评分。  
- [llm.py](./llm.py): 初始化大模型的接口。  
- [load_data.py](./load_data.py): 加载知识图谱接口。
- [requirements.txt](./requirements.txt): python环境依赖文件

可以通过下列命令运行该测试demo
```
bash run.sh
```
[run.sh](./run.sh)中的参数```path```是测试文件所在的路径，```llm```为本地大模型所在路径.  
医学问题数据集来自于 [CMB](https://github.com/FreedomIntelligence/CMB?tab=readme-ov-file)，可以下载并替换```./train.json```文件。
