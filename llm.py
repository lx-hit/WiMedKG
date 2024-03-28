import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, AutoModel
from transformers.generation.utils import GenerationConfig


class ChatGLM_LLM():

    def init_LLM(self, model_dir):
        self.tokenizer = AutoTokenizer.from_pretrained(model_dir, use_fast=False, trust_remote_code=True)
        # self.model = AutoModelForCausalLM.from_pretrained(model_dir, device_map="auto", torch_dtype=torch.bfloat16, trust_remote_code=True)
        self.model = AutoModel.from_pretrained(model_dir, trust_remote_code=True).half().cuda()
        self.model = self.model.eval()
        # self.model.generation_config = GenerationConfig.from_pretrained(model_dir)

    def query(self, message):
        # messages = []
        # messages.append({"role": "user", "content": message})
        # response = self.model.chat(self.tokenizer, messages)
        response, history = self.model.chat(self.tokenizer, message, history=[])
        return response

class BaiChuan_LLM():

    def init_LLM(self, model_dir):
        self.tokenizer = AutoTokenizer.from_pretrained(model_dir, use_fast=False, trust_remote_code=True)
        self.model = AutoModelForCausalLM.from_pretrained(model_dir, device_map="auto", torch_dtype=torch.bfloat16, trust_remote_code=True)
        self.model.generation_config = GenerationConfig.from_pretrained(model_dir)

    def query(self, message):
        messages = []
        messages.append({"role": "user", "content": message})
        response = self.model.chat(self.tokenizer, messages)
        return response