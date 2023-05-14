import telebot
from telebot import types
from selenium import webdriver
from bs4 import BeautifulSoup as bs
import time

token = '6277616731:AAE04mifGpHzIYetLP3jyRPGIOAOPSLFzTk'
bot = telebot.TeleBot(token, parse_mode='html')


@bot.message_handler(commands=['start']) # Приветствие
def start_message(message):
    bot.send_message(message.chat.id, 'Привет! Я помогу промониторить курс доллара. Введите /menu')


@bot.message_handler(commands=['menu']) # Кнопки
def button_message(message):
    markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
    dollar_course_down=types.KeyboardButton("Задать нижнюю границу доллара")
    dollar_course_up=types.KeyboardButton("Задать верхнюю границу доллара")
    monitoring_start=types.KeyboardButton("Запустить мониторинг")
    sleep_time = types.KeyboardButton("Задать промежуток уведомлений")
    markup.add(dollar_course_down, dollar_course_up, monitoring_start, sleep_time)
    bot.send_message(message.chat.id, 'Для начала задайте нужную границу.', reply_markup=markup)

@bot.message_handler(content_types=['text'])
def main(message):
    if message.text == "Задать нижнюю границу доллара" :
        bot.send_message(message.chat.id, 'Введите нижнюю границу доллара.')
        bot.register_next_step_handler(message, low_tab)
    if message.text == "Задать верхнюю границу доллара" :
        bot.send_message(message.chat.id, 'Введите верхнюю границу доллара.')
        bot.register_next_step_handler(message, high_tab)
    if message.text == "Запустить мониторинг" :
        bot.send_message(message.chat.id, 'Запускаю мониторинг..', reply_markup=types.ReplyKeyboardRemove())
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        breaking = types.KeyboardButton("Остановить мониторинг")
        markup.add(breaking)
        time.sleep(1.5)
        bot.send_message(message.chat.id, 'Для остановки мониторинга нажмите соответствующую кнопку.', reply_markup=markup)
        while True:
            r_course = parsing()
            if r_course > high_bracket:
                bot.send_message(message.chat.id, "Доллар выше границы на {:.2f} рублей".format(r_course-high_bracket))
            if r_course < low_bracket:
                bot.send_message(message.chat.id, 'Доллар ниже границы на {:.2f} руб'.format(low_bracket-r_course))
            time.sleep(interval)
    if message.text == "Задать промежуток уведомлений":
        bot.send_message(message.chat.id, 'Введите интервал в часах')
        bot.register_next_step_handler(message, time_interval)


def low_tab(message):
    try:
        low = message.text
        if not low.isdigit():
            message = bot.send_message(message.chat.id, 'Введите заново')
            bot.register_next_step_handler(message, low_tab)
        global low_bracket
        low_bracket = low
        if ',' in low_bracket:
            low_bracket = low_bracket.replace(',', '.')
        low_bracket = float(low_bracket)
        bot.send_message(message.chat.id, 'Нижняя граница определена : {} руб'.format(low_bracket))
    except Exception as e:
        bot.send_message(message.chat.id, "Что-то пошло не так..")

def high_tab(message):
    try:
        high = message.text
        if not high.isdigit():
            message = bot.send_message(message.chat.id, 'Введите заново')
            bot.register_next_step_handler(message, high_tab)
        global high_bracket
        high_bracket = high
        if ',' in high_bracket:
            high_bracket = high_bracket.replace(',', '.')
        high_bracket = float(high_bracket)
        bot.send_message(message.chat.id, 'Верхняя граница определена : {} руб'.format(high_bracket))
    except Exception as e:
        bot.send_message(message.chat.id, "Что-то пошло не так..")
        
def time_interval(message):
    time = message.text
    global interval
    interval = float(time)
    bot.send_message(message.chat.id, 'Бот будет проверять доллар каждые {} часа(ов)'.format(interval))
    interval = interval * 3600

def parsing(): #исполняющая парсинг-функция
            browser = webdriver.Chrome()
            browser.get("https://www.banki.ru/products/currency/cash/omsk/")
            source_data = browser.page_source
            soup = bs(source_data, features='html.parser')
            categories = soup.find('div', {'class': ['table-flex__cell table-flex__cell--without-padding padding-left-default']})
            course = categories.text
            if ',' in course:
                course = course.replace(',', '.')
                course = float(course)
            return course


bot.infinity_polling()

