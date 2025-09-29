# Evaluation of CAIM on GVD
import json
from Components.memory_processing import generate_new_memories, save_memory
from Components.controller_agent import controller_agent

# method to fill each memory of each virtual user of GVD
def fill_evaluation_memories():
    with open('Evaluation/eval_data/memory_bank_en.json', 'r', encoding='utf-8') as mb_file:
            memory_bank = json.load(mb_file)

    # save conversation contex of each person as inductive thoughts in seperate memory
    for person_key, person_data in memory_bank.items():
        name = person_data.get("name")

        for date, conversations in person_data.get("history", {}).items():
            short_term_memory = []
            daily_memory = {
                "date": date,
                "name":  name,
                "conversation": conversations
            }
            
            short_term_memory.append(daily_memory)
            pre_processed_memory = generate_new_memories(short_term_memory)
            tags_to_review = save_memory(pre_processed_memory, 'Evaluation/gpt4o/Memory_gpt4o/memory_' + name.lower() + '.csv')


# method to answer probing questions for each virtual user of GVD
def answer_probing_questions(system_prompt):
     # answer eval questions
    with open('Evaluation/eval_data/probing_questions_en.json', 'r', encoding='utf-8') as question_file:
        question_data = json.load(question_file)
    
    for person, questions in question_data.items():
        short_term_memory = []
        memory = 'Evaluation/gpt4o/Memory_gpt4o/memory_' + person.lower() + '.csv'

        for question in questions:
            print(question)
            controller_agent(question, short_term_memory, system_prompt, memory)

        output_file = 'Evaluation/gpt4o/evaluation/evaluation_' + person.lower() + '.json'
        with open(output_file, "w", encoding="utf-8") as file:
            json.dump(short_term_memory, file, indent=4, ensure_ascii=False)
        break