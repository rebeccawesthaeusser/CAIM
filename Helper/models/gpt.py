from openai import AzureOpenAI

from Helper.helper import get_keys

# get GPT response
def api_call(init_prompt, task):
    keys = get_keys('gpt4o')

    client = AzureOpenAI(
        api_version = keys['api_version'],
        azure_endpoint = keys['azure_endpoint'],
        api_key = keys['api_key'],
    )
    
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": init_prompt,
            },
            {
                "role": "user",
                "content": task,
            }
        ]
    )

    return response.choices[0].message.content