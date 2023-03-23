import telebot
from telebot import types
from selenium import webdriver
from bs4 import BeautifulSoup as bs

token = '6277616731:AAE04mifGpHzIYetLP3jyRPGIOAOPSLFzTk'
bot = telebot.TeleBot(token, parse_mode='html')

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Привет! /menu для выбора задания')

@bot.message_handler(commands=['menu'])
def button_message(message):
    markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
    dollar_course=types.KeyboardButton("Узнать курс доллара")
    markup.add(dollar_course)
    bot.send_message(message.chat.id, 'Выберите что вам надо', reply_markup=markup)

@bot.message_handler(content_types='text')
def message_reply(message):
    if message.text == "Узнать курс доллара":
        def parse():
            browser = webdriver.Chrome()
            browser.get("https://www.banki.ru/products/currency/cash/omsk/")
            source_data = browser.page_source
            soup = bs(source_data, features='html.parser')
            categories = soup.find('div', {'class': ['table-flex__cell table-flex__cell--without-padding padding-left-default']})
            course = categories.text
            if ',' in course:
                course = course.replace(',', '.')
                course = float(course)
                if course > 80.0:
                    bot.send_message(message.chat.id, "Доллар стал выше 80!")
                if course < 70.0:
                    bot.send_message(message.chat.id, "Доллар резко упал ниже 70!")
            return categories.text

        enter = parse()
        bot.send_message(message.chat.id, enter + ' рублей')

bot.infinity_polling()