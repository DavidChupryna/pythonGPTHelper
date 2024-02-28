import logging
import requests
from transformers import AutoTokenizer
from config import config

max_tokens = int(config['GPT']['MAX_MESSAGE_TOKENS'])

logging.basicConfig(
    level=config['LOGGING']['level'],
    format=config['LOGGING']['format'],
    filename=config['LOGGING']['filename'],
    filemode=config['LOGGING']['filemod']
)

say_continue = ['продолжить', 'продолжи', 'продолжи ответ', 'next', 'далее']


def count_token(text):
    tokenizers = AutoTokenizer.from_pretrained("mistralai/Mistral-7B-Instruct-v0.2")
    return len(tokenizers.encode(text))


def create_prompt(user_request, answer, assistant_content):
    json = {
        "messages": [
            {
                "role": "system",
                "content": "Отвечай как русский учитель по языку программирования Python, а также поддерживай "
                           "разговор с пользователем."
            },
            {
                "role": "user",
                "content": user_request
            },
            {
                "role": "assistant",
                "content": assistant_content + answer
            }
        ],
        "temperature": config['GPT']['TEMPERATURE'],
        "max_tokens": config['GPT']['MAX_TOKENS']
    }
    return json


def error_handler(resp):
    if resp.status_code < 200 or resp.status_code >= 300:
        logging.error(resp.status_code)
        return False

    try:
        success_response = resp.json()
    except:
        logging.error('Error receiving JSON')
        return False

    if 'error' in success_response:
        logging.error(success_response['error'])
        return False

    return success_response


answer = ""


def send_request(task):
    global answer

    if count_token(task) > max_tokens:
        logging.warning("The request exceeds the token limit")
        return "Запрос слишком длинный"

    else:
        if task in say_continue:
            assistant_content = "Решим задачу по шагам: " + answer

        else:
            answer = ""
            assistant_content = "Решим задачу по шагам: "

        resp = requests.post(
            url=config['GPT']['URL'],
            headers={"Content-Type": "application/json"},
            json=create_prompt(task, answer, assistant_content))

    full_response = error_handler(resp)

    if not full_response:
        return False

    message = full_response['choices'][0]['message']['content']
    answer += message
    return answer

