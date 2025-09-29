from Helper.models.gpt import api_call
from Helper.helper import get_date, get_prompt
from Components.controller_agent import is_information_necessary, controller_agent
from Components.memory_processing import memory_processing
from Evaluation.evaluation_methods import fill_evaluation_memories, answer_probing_questions

# execute program
def main():
    short_term_memory = []

    print("Type 'exit' to stop the program")
    while True:
      response = api_input(input("User: "), short_term_memory)
      if response == 'exit':
          False


def api_input(user_input: str, short_term_memory: list, memory_file = 'Memory/memory.csv'):
    system_prompt = get_prompt('response_generator', 'general_response')

    # memory processing step
    if user_input.lower() == 'exit':
        memory_processing(short_term_memory, memory_file)
        return 'exit'

    # Evaluation: fill memories
    elif user_input.lower() == 'eval':
        fill_evaluation_memories()
                               
    # Evaluation: answer probing questions
    elif user_input.lower() == 'questions':
        answer_probing_questions(system_prompt)

    # normal chat
    else:
        return controller_unit(user_input, short_term_memory, system_prompt, memory_file)        


# controller unit to get matching memories and generate an appropriate response
def controller_unit(user_input, short_term_memory, system_prompt, memory_file):
    
    if is_information_necessary(user_input):
        system_prompt = controller_agent(user_input, short_term_memory, memory_file)

    response = api_call(system_prompt, user_input)
    print("GPT: ", response)

    # save ongoing conversation in list
    short_term_memory.append(
        [
            {"role": "User", "content": user_input },
            {"role": "AI-assistant", "content": response},
            {"timestamp": get_date()}
        ]
    )
    return response


if __name__ == "__main__":
    main()
