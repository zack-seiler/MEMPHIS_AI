import os
import openai


def read_token():
    file_name = "OpenAI_API_Key.txt"
    current_dir = os.getcwd()
    file_path = os.path.join(current_dir, file_name)
    with open(file_path, 'r') as file:
        token = file.readline().strip()
    return token


openai.api_key = read_token()

message_array = [
    {"role": "system", "content": "You are an assistant named Memphis. Please provide your responses in a witty and "
                                  "sarcastic manner. However, remember to remain helpful and accurate. You know when "
                                  "its time to be serious, and when it's okay to goof around a bit. Please always "
                                  "address your user as \"sir\", and give the shortest responses possible. Do not "
                                  "answer any question not asked directly, and do not provide abundant elaboration."},
]


def get_response(user_prompt):
    message_array.append({"role": "user", "content": user_prompt})
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=message_array
    )
    message_array.append(completion.choices[0].message)
    return completion.choices[0].message.content
