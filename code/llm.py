import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, AutoModel
from transformers.generation.utils import GenerationConfig
from openai import OpenAI


class ChatGLM_LLM():

    def __init__(self, model_dir):
        self.tokenizer = AutoTokenizer.from_pretrained(model_dir, use_fast=False, trust_remote_code=True)
        self.model = AutoModel.from_pretrained(model_dir, trust_remote_code=True).half().cuda()
        self.model = self.model.eval()

    def query(self, message):
        response, history = self.model.chat(self.tokenizer, message, history=[])
        return response

class BaiChuan_LLM():

    def __init__(self, model_dir):
        self.tokenizer = AutoTokenizer.from_pretrained(model_dir, use_fast=False, trust_remote_code=True)
        self.model = AutoModelForCausalLM.from_pretrained(model_dir, device_map="auto", torch_dtype=torch.bfloat16, trust_remote_code=True)
        self.model.generation_config = GenerationConfig.from_pretrained(model_dir)

    def query(self, message):
        messages = []
        messages.append({"role": "user", "content": message})
        response = self.model.chat(self.tokenizer, messages)
        return response

class api_LLM():

    def __init__(self):
        self.client = OpenAI(
            api_key="EMPTY",
            base_url="http://0.0.0.0:8000/v1",
        )
        self.models = self.client.models.list()
        print(self.models.model_dump())

    def query(self, message):
        chat_completion = self.client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": message,
                }
            ],
            model="gpt-3.5-turbo",
        )                   
        return chat_completion.choices[0].message.content