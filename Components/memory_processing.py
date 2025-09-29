# Memory Processing based on Think-in-Memory (TiM)
import json
import os
import pandas as pd

from Helper.helper import generate_conversation_string, split_string_by_Z, get_date, get_prompt, get_ontology
from Helper.models.gpt import api_call

# function to extract relevant items from conversation history
def get_relevant_items_of_conversation(short_term_memory):
    conversation_string = generate_conversation_string(short_term_memory) 
    relevant_items = api_call(get_prompt('memory_processing', 'summary_agent'), conversation_string + get_date()) 
    
    # update ontology if necessary
    expand_ontology(relevant_items)
    return relevant_items

# function to select 3 tags and one inductive thought for every relevant item
def generate_new_memories(short_term_memory):
    relevant_items = get_relevant_items_of_conversation(short_term_memory)
    new_memories = api_call(get_prompt('memory_processing', 'memory_agent') + get_ontology(), relevant_items)
    return split_string_by_Z(new_memories)

# function to store new memories in LTM
def save_memory(pre_processed_memory, file):
    if not os.path.exists(file):
        pd.DataFrame(columns=["tag", "inductive thought", "timestamp"]).to_csv(file, sep=';', index=False)

    # load existing memory and new data as dataframe
    existing_memory = pd.read_csv(file, delimiter=';')
    new_memories = []
    tags = []

    # split memory list after each semicolon to separate entries => tag1,tag2,tag3;inductive thought;timestamp
    for memory in pre_processed_memory:
        parts = memory.split(';')
        tags.extend(parts[0].split(',')) # save tags to remove duplicates later
        if len(parts) > 1:
            new_memories.append([parts[0], parts[1], parts[2]])

    new_memory_data = pd.DataFrame(new_memories, columns=['tag', 'inductive thought', 'timestamp'])

    # append and save new data
    df_combined = pd.concat([existing_memory, new_memory_data], ignore_index=True)
    df_combined.to_csv(file, index=False, sep=';')

    return pd.Series(tags).unique().tolist()


# Review Agent => delete/merge duplicates
def merge_duplicates(tags_to_review, file):
    memory = pd.read_csv(file, sep=';')
    filtered_data = []
    rows_to_drop = []

    # get every row with tags that were newly saved in memory 
    for index, row in memory.iterrows():
        row_tags = row['tag'].split(',')
        if any(tag in tags_to_review for tag in row_tags):
            filtered_data.append(row.to_dict())
            rows_to_drop.append(index)

    # delete rows in memory that Agent merges / deletes
    memory.drop(rows_to_drop, inplace=True)
    memory.to_csv(file, index=False, sep=';')
    
    # let Agent remove duplicates
    updated_memories = api_call(get_prompt('memory_processing', 'review_agent'), ''.join(str(entry) for entry in filtered_data))
    save_memory(split_string_by_Z(updated_memories), file)


# function to expand ontology
def expand_ontology(relevant_items):
    response = api_call(get_prompt('memory_processing', 'expand_ontology') + get_ontology(), relevant_items)

    # overwrite current ontology with updated ontology
    if response != 'OK':
        new_ontology = json.loads(response)
        with open('ontology.json', 'w') as json_file:
            json.dump(new_ontology, json_file, indent=4)


# main method of Memory Processing step
def memory_processing(short_term_memory, memory_file):
    pre_processed_memory = generate_new_memories(short_term_memory)
    tags_to_review = save_memory(pre_processed_memory, memory_file)
    merge_duplicates(tags_to_review, memory_file)