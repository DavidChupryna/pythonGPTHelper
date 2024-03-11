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


def select_system_role(task: str, level: str):
    if task == 'Python':
        if level == 'Начальный':
            role_system = config['TEMPLATE_GPT']['PYTHON_BEGINNER']
            return role_system
        elif level == 'Продвинутый':
            role_system = config['TEMPLATE_GPT']['PYTHON_ADVANCED']
            return role_system
    elif task == 'JavaScript':
        if level == 'Начальный':
            role_system = config['TEMPLATE_GPT']['JAVA_SCRIPT_BEGINNER']
            return role_system
        elif level == 'Продвинутый':
            role_system = config['TEMPLATE_GPT']['JAVA_SCRIPT_ADVANCED']
            return role_system
    else:
        return 'Введите коректный запрос.'


def create_prompt(user_request, assistant_content, role_system):
    json = {
        "messages": [
            {
                "role": "system",
                "content": role_system
            },
            {
                "role": "user",
                "content": user_request
            },
            {
                "role": "assistant",
                "content": assistant_content
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


def send_request(task, system_role):
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
            json=create_prompt(task, assistant_content, system_role))

    full_response = error_handler(resp)

    if not full_response:
        return False

    message = full_response['choices'][0]['message']['content']
    answer += message
    return answer
