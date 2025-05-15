[Chinese ver.](./README_CH.md)

- [get_path.py](./get_path.py): Retrieves one-hop and two-hop paths related to the question in the knowledge graph.
- [generate_new_answer.py](./generate_new_answer.py): Uniformly samples a certain number of knowledge paths from the identified paths and incorporates them into the prompt to assist the large model in generating an answer.  
- [eval.py](./eval.py): Scores the answers produced by the model.  
- [llm.py](./llm.py): Initializes the interface for the large language model.  
- [load_data.py](./load_data.py): Loads the knowledge graph interface.  
- [requirements.txt](./requirements.txt): A file listing Python environment dependencies.

You can run this test demo using the following command:
```
bash run.sh
```

The parameter ```path``` in [run.sh](./run.sh) specifies the path to the test files, and ```llm``` specifies the path to the local large model.  
The medical question dataset comes from [CMB](https://github.com/FreedomIntelligence/CMB?tab=readme-ov-file), and you can download it and replace the ```./train.json``` file with it.