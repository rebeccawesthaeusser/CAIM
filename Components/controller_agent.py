# Controller Agent based on SCM (Self-Controlled Memory)
from Components.memory_retrieval import memory_retrieval
from Helper.helper import generate_conversation_string, get_prompt, is_summary_necessary
from Helper.models.gpt import api_call

### Decision Unit Prompts
# function to let Controller Agent decide whether a further information is necessary
def is_information_necessary(user_input):
    answer = api_call(get_prompt('controller_agent', 'is_information_necessary'), user_input)
    return True if answer == 'A' else False

# function to let Controller Agent decide whether a memory retrieval and conversation context is necessary
def is_memory_and_context_necessary(user_input):
    answer = api_call(get_prompt('controller_agent', 'is_memory_and_context_necessary'), user_input)
    return True if answer == 'A' else False

# function to let Controller Agent decide whether a memory retrieval is necessary
def is_memory_retrieval_necessary(user_input):
    answer = api_call(get_prompt('controller_agent', 'is_memory_necessary'), user_input)
    return True if answer == 'A' else False


# conversation context: summary or full conversation
def get_conversation_context(short_term_memory):
    if (is_summary_necessary(short_term_memory)):
        conversation_string = generate_conversation_string(short_term_memory) 
        summary = api_call(get_prompt('controller_agent', 'get_summary'), conversation_string) 
        return summary
    else:
        conversation_string = generate_conversation_string(short_term_memory)
        return conversation_string


# main method of Controller Agent
def controller_agent(user_input, short_term_memory, memory_file):
    memory_list = ''
    system_prompt = ''
    
    # case 1: memory and conversation context
    if(is_memory_and_context_necessary(user_input)):
        memory_list = memory_retrieval(user_input, memory_file)
        conversation = get_conversation_context(short_term_memory)
        system_prompt = get_prompt('response_generator', 'memory_and_conversation_response') + ', List of historical previous information: ' + ', '.join(memory_list) + ', History of conversation: ' + conversation

    # case 2: memory retrieval
    elif(is_memory_retrieval_necessary(user_input)):
        memory_list = memory_retrieval(user_input, memory_file)
        system_prompt = get_prompt('response_generator','memory_response') + ', '.join(memory_list)

    # case 3: conversation history
    else:
        conversation = get_conversation_context(short_term_memory)
        system_prompt = get_prompt('response_generator', 'conversation_response') + conversation
    
    return system_prompt