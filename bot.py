import telebot
from config import token
from data import load_user_data, save_user_data

bot = telebot.TeleBot(token=token)

data_path = 'users.json'
user_data = load_user_data(data_path)