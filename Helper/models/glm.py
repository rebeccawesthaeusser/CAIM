import torch
from transformers import AutoTokenizer, AutoModel
import os

os.environ["CUDA_LAUNCH_BLOCKING"] = "1"

tokenizer = AutoTokenizer.from_pretrained("THUDM/chatglm-6b", trust_remote_code=True)
model = AutoModel.from_pretrained("THUDM/chatglm-6b", trust_remote_code=True).half().cuda()

def api_call(init_prompt, task, optional = ''):
    torch.cuda.empty_cache()
    
    input = init_prompt + task

    with torch.no_grad():
        if optional != "":
            response, history = model.chat(tokenizer, input, history=[optional])
        else:
            response, history = model.chat(tokenizer, input, history=[])

    return response
