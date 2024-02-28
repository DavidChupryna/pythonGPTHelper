import logging
import telebot
from config import token
from data import load_user_data, save_user_data
from gpt import send_request

bot = telebot.TeleBot(token=token)

data_path = 'users.json'
user_data = load_user_data(data_path)


@bot.message_handler(commands=['start'])
def say_start(message):
    bot.send_message(message.chat.id, "Привет! Я GPT хелпер по языку программирования Python🐍. \n"
                                      "Для полного ознакопления с ботом, воспользуйтесь командой /help")
    logging.info("Say start")
    user_id = str(message.from_user.id)
    if user_id not in user_data:
        user_data[user_id] = {}
        user_data[user_id]['username'] = message.from_user.first_name
        save_user_data(user_data, data_path)
    elif user_id in user_data:
        bot.send_message(message.chat.id,f"{message.from_user.first_name} рад вас снова видеть!")


@bot.message_handler(commands=['help'])
def say_help(message):
    bot.send_message(message.chat.id, "Я GPT хелпер по языку программирования Python, а также хороший собеседник по программированию.\n"
                                      "В боте есть ограничение символов на запрос, не рассписывай слишком большие запросы.\n"
                                      "Нейросеть отвечает частями и если тебе мало информации или хочешь узнать "
                                      "что-то подробнее, напиши в чат ('продолжить', 'продолжи', 'продолжи ответ', 'next', 'далее')\n"
                                      "Полный список команд: \n"
                                      "/start - начать все сначала.\n"
                                      "/help - подробная информация о боте.\n"
                                      "/start_gpt - начать работу с нейросетью.")


@bot.message_handler(commands=['debug'])
def send_logs(message):
    with open("log_file.txt", "rb") as f:
        bot.send_document(message.chat.id, f)
        logging.info("Use command DEBUG")


@bot.message_handler(commands=['start_gpt'])
def start_gpt(message):
    user_id = message.from_user.id
    bot.send_message(user_id, f"{message.from_user.first_name} cледующим сообщением напиши запрос нейросети.")
    bot.register_next_step_handler(message, send_task)


def send_task(message):
    user_id = message.from_user.id
    user_prompt = message.text.lower()
    if user_prompt in ['/start', '/help', '/debug']:
        bot.send_message(user_id, "В режиме запроса к нейросети, команды не работают. Воспользуйтесь ими повторно: \n"
                                  "/start \n"
                                  "/help ")
        return
    gpt_response = send_request(user_prompt)
    logging.info("Send task to GPT")
    if gpt_response:
        if gpt_response == "":
            bot.send_message(user_id, "Ответ на ваш вопрос полностью сгенирирован. Задайте слеующий!")
        else:
            bot.send_message(user_id, gpt_response)
            bot.send_message(user_id, "Если хочешь продолжение ответа, напиши: 'продолжить' или 'далее'.")
            logging.info("GPT send answer")
    else:
        bot.send_message(user_id, "Произошла ошибка")

    bot.register_next_step_handler(message, send_task)


@bot.message_handler(content_types=['text'])
def solve_task_not_running(message):
    bot.send_message(message.chat.id, "Для начала работы с нейросетью, воспользуйтесь командой /start_gpt")


bot.polling()