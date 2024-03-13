import logging
import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from config import token
from database import create_table, update_data, insert_data, get_data, delete_data
from gpt import send_request, select_system_role

bot = telebot.TeleBot(token=token)


def create_buttons(list_buttons: list):
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
    for button in list_buttons:
        keyboard.add(KeyboardButton(button))

    return keyboard


@bot.message_handler(commands=['start'])
def say_start(message):
    bot.send_message(message.chat.id, "Привет! Я GPT хелпер по языкам программирования Python🐍 и JavaScript. \n"
                                      "Для полного ознакопления с ботом, воспользуйтесь командой /help")

    logging.info("Say start")
    create_table()


@bot.message_handler(commands=['help'])
def say_help(message):
    bot.send_message(message.chat.id, "Я GPT хелпер по языкам программирования Python и JavaScript, а также хороший помошник.\n"
                                      "В боте есть ограничение символов на запрос, не рассписывай слишком большие запросы.\n"
                                      "Нейросеть отвечает частями и если тебе мало информации или хочешь узнать "
                                      "что-то подробнее, напиши в чат ('продолжить', 'продолжи', 'продолжи ответ', 'next', 'далее')\n"
                                      "Полный список команд: \n"
                                      "/start - начать все сначала.\n"
                                      "/help - подробная информация о боте.\n"
                                      "/start_gpt - начать работу с нейросетью.\n"
                                      "/stop - остонавливает работу с GPT")


@bot.message_handler(commands=['debug'])
def send_logs(message):
    with open("log_file.txt", "rb") as f:
        bot.send_document(message.chat.id, f)
        logging.info("Use command DEBUG")


@bot.message_handler(commands=['start_gpt'])
def choice_subject(message):
    user_id = message.from_user.id
    user_name = message.from_user.first_name
    delete_data(user_id)
    keyboard = create_buttons(['Python', 'JavaScript'])
    insert_data(user_id, user_name)
    bot.send_message(message.chat.id, 'Выберете язык программирования, по которому вам нужна помощь.',
                     reply_markup=keyboard)


@bot.message_handler(func=lambda message: message.text in ['Python', 'JavaScript'])
def select_level(message):
    user_id = message.from_user.id
    keyboard = create_buttons(['Начальный', 'Продвинутый'])
    bot.send_message(message.chat.id, f'Вы выбрали предмет {message.text}. Теперь выберете уровень объяснения',
                     reply_markup=keyboard)
    subject = message.text
    update_data(user_id, 'subject', subject)


@bot.message_handler(func=lambda message: message.text in ['Начальный', 'Продвинутый'])
def solve_task(message):
    user_id = message.from_user.id
    level = message.text
    bot.send_message(user_id, f"{message.from_user.first_name}, вы выбрали {level} уровень. Следующим сообщением "
                              f"напишите запрос нейросети.",
                     reply_markup=ReplyKeyboardRemove())
    update_data(user_id, 'level', level)
    bot.register_next_step_handler(message, send_task)


def send_task(message):
    user_id = message.from_user.id
    user_name = message.from_user.first_name

    user_prompt = message.text.lower()
    user = get_data()
    role = select_system_role(user['subject'], user['level'])

    if user_prompt in ['/start', '/help', '/debug', '/start_gpt']:
        bot.send_message(user_id, "В режиме запроса к нейросети, команды не работают. Воспользуйтесь ими повторно: \n"
                                  "/start \n"
                                  "/help ")
        return
    elif user_prompt == '/stop':
        bot.send_message(user_id, 'Нейросеть закончила работу. Для начала работы заново, воспользуйтесь командой '
                                  '/start_gpt')
        return

    gpt_response = send_request(user_prompt, role)
    insert_data(user_id, user_name, user['subject'], user['level'], user_prompt, gpt_response)
    logging.info("Send task to GPT")

    if gpt_response:
        if gpt_response == "":
            bot.send_message(user_id, "Ответ на ваш вопрос полностью сгенирирован. Задайте слеующий!")
        else:
            bot.send_message(user_id, gpt_response)
            bot.send_message(user_id, f"Если хочешь продолжение ответа, напиши: 'продолжить' или 'далее'.\n"
                                      f"А если хотите задать новый вопрос, напишете его в чат!.")
            logging.info("GPT send answer")
    else:
        bot.send_message(user_id, "Произошла ошибка")

    bot.register_next_step_handler(message, send_task)


@bot.message_handler(content_types=['text'])
def solve_task_not_running(message):
    bot.send_message(message.chat.id, "Для начала работы с нейросетью, воспользуйтесь командой /start_gpt")


bot.polling()