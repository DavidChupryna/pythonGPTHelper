import telebot
from config import token
from data import load_user_data, save_user_data
from gpt import send_request

bot = telebot.TeleBot(token=token)

data_path = 'users.json'
user_data = load_user_data(data_path)


@bot.message_handler(commands=['start'])
def say_start(message):
    bot.send_message(message.chat.id, "Привет")


@bot.message_handler(commands=['solve_task'])
def solve_task(message):
    user_id = message.from_user.id
    bot.send_message(user_id, "Следующим сообщением напиши промпт")
    bot.register_next_step_handler(message, send_task)


@bot.message_handler(content_types=['text'])
def send_task(message):
    user_id = message.from_user.id
    user_prompt = message.text
    gpt_response = send_request(user_prompt)
    if gpt_response:
        bot.send_message(user_id, gpt_response)
    else:
        bot.send_message(user_id, "Произошла ошибка")



bot.polling()