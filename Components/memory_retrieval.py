# Retrieval Process
import pandas as pd

from Helper.helper import get_date, get_prompt, get_ontology
from Helper.models.gpt import api_call


# let Tagging Agent select up to three tags from an ontology
def tagging_agent(user_input):
    tags = api_call(get_prompt('memory_retrieval', 'tagging_agent') + get_ontology(), user_input)
    return [tag.strip() for tag in tags.split(",")]


# filter memory by tags to get memories based on user input
def retrieve_memories(tags, user_input, file, timestamps=[]):
    relevant_memory = []
    thoughts = ''
    df = pd.read_csv(file, delimiter=";")

    # Loop over all tags to get inductive thoughts
    for tag in tags:
        try:
            filtered_df_tags = df[df['tag'].apply(lambda tag_list: tag.lower() in tag_list)]
            inductive_thoughts_with_timestamps = filtered_df_tags.apply(lambda row: f"{row['inductive thought']} ({row['timestamp']})", axis=1)
            result_string = ', '.join(inductive_thoughts_with_timestamps)
            thoughts += result_string

        except (pd.errors.EmptyDataError, KeyError, TypeError):
            print("No data.")

    # Let Filtering Agent decide inductive thoughts relevant based on the user input
    if thoughts:
        relevant_thoughts = api_call(get_prompt('memory_retrieval', 'filtering_agent') + thoughts, user_input) 
        relevant_memory += [thought.strip() for thought in relevant_thoughts.split(", ")]

     # Loop over all timestamps to get inductive thoughts
    for timestamp in timestamps:
        try:
            filtered_df_timestamps = df[df['timestamp'].apply(lambda timestamp_list: timestamp in timestamp_list)]
            inductive_thoughts_with_timestamps = filtered_df_timestamps.apply(lambda row: f"{row['inductive thought']} ({row['timestamp']})", axis=1)
            result_string = ', '.join(inductive_thoughts_with_timestamps)
            relevant_memory += [thought.strip() for thought in result_string.split(", ")]

        except (pd.errors.EmptyDataError, KeyError, TypeError):
            print("No data.")

    # Return the relevant memories
    return relevant_memory if len(relevant_memory) > 0 else "You don't have enough information to respond correctly."


def is_temporal_unit_present(user_input):
    answer = api_call(get_prompt('memory_retrieval', 'is_temporal_unit_present'), user_input) 
    return True if answer == 'A' else False


# memory retrieval main method: get specific memories based on tags
def memory_retrieval(user_input, file):
    timestamps = []

    if(is_temporal_unit_present(user_input)):
        temporal_units = api_call(get_prompt('memory_retrieval', 'time_agent') + get_date(), user_input) 
        timestamps += [unit.strip() for unit in temporal_units.split(",")]
    
    tags = tagging_agent(user_input)
    memory_list = retrieve_memories(tags, user_input, file, timestamps)

    return memory_list
