import datetime
import json
from transformers import GPT2Tokenizer

# function to convert current_conversation list to string
def generate_conversation_string(current_conversation):
    flat_conversation = [message for conversation in current_conversation for message in conversation]
    conversation_string = ""
    
    # Iterate through the flat conversation and remove json structure
    for i, message in enumerate(flat_conversation):
        if 'role' in message and 'content' in message:
            conversation_string += ' ' + f"{message['role']}: {message['content']}"

    return conversation_string


# function to split list entries by Z, then add Z again
def split_string_by_Z(list):
    splitted_list = [memory.strip() for memory in list.split("Z,")]
    return [entry if entry.endswith('Z') else entry + 'Z' for entry in splitted_list]


# function to get current date
def get_date():
    return datetime.datetime.now(datetime.UTC).strftime("%Y-%m-%dZ")

# function to get API keys
def get_keys(model_name):
    with open("helper/api_keys.json") as f:
        keys = json.load(f)

    return keys[model_name]

# function to get specific prompt from prompts.json
def get_prompt(category: str, name: str) -> str:
    with open('helper/prompts.json', encoding='utf-8') as f:
        prompts = json.load(f)

    prompt = prompts[category][name]
    return prompt


# function to get ontology from ontology.json
def get_ontology() -> str:
    with open('helper/ontology.json', encoding='utf-8') as f:
        ontology = json.load(f)
    return json.dumps(ontology)

# function to count the amount of tokens in a list of memories
def is_summary_necessary(current_conversation):
    tokenizer = GPT2Tokenizer.from_pretrained('gpt2')
    total_tokens = 0

    for conversation in current_conversation:
        for message in conversation:
            if 'role' in message and 'content' in message:
                total_tokens += len(tokenizer.encode(f"{message['role']}: {message['content']}"))
            if 'timestamp' in message:
                total_tokens += len(tokenizer.encode(f"timestamp: {message['timestamp']}"))

    return True if total_tokens > 2000 else False