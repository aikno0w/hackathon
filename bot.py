import telebot
from telebot import types
import logging
import time

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

# Replace with your bot token from BotFather
API_TOKEN = '6518553338:AAHhTUU9rnQQxMgPf343UQ-6uAnLyBKa9U8'
bot = telebot.TeleBot(API_TOKEN)

# Channels
channel_events = '@buddy_events'
channel_charity = '@buddy_charity'

# Dictionary to store the event descriptions for users
user_event_data = {}
user_pet_data = {}
psychologist_data = {}

# Main Menu: Display options like Мероприятия, Благотворительная помощь, etc.
@bot.message_handler(commands=['start'])
def send_welcome(message):
    logger.info("Starting buttons")
    markup = types.ReplyKeyboardMarkup(row_width=1)
    btn1 = types.KeyboardButton('Мероприятия')
    btn2 = types.KeyboardButton('Благотворительная помощь')
    btn3 = types.KeyboardButton('Психологическая помощь')
    markup.add(btn1, btn2, btn3)

    bot.send_message(
        message.chat.id, 
        f"Привет, {message.from_user.first_name}! Добро пожаловать в Buddy bot для поиска мероприятий и волонтеров.\n"
        "Выбери подходящую опцию:",
        reply_markup=markup
    )

# Handling Благотворительная помощь Section
@bot.message_handler(func=lambda message: message.text in ['Благотворительная помощь', 'Выложить объявление', 'Открыть список объявлений'])
def handle_pets(message):
    if message.text == 'Благотворительная помощь':
        pets(message)
    elif message.text == 'Выложить объявление':
        reg_pet(message)
    elif message.text == 'Открыть список объявлений':
        bot.send_message(message.chat.id, "Перейти на канал с объявлениями: @buddy_charity")
    else:
        bot.send_message(message.chat.id, "Повторите попытку.")

def pets(message):
    markup = types.ReplyKeyboardMarkup(row_width=1)
    btn1 = types.KeyboardButton('Выложить объявление')
    btn2 = types.KeyboardButton('Открыть список объявлений')
    btn_back = types.KeyboardButton('Назад')  # "Назад" button
    markup.add(btn1, btn2, btn_back)
    bot.send_message(
        message.chat.id,
        "Выбери подходящую опцию:",
        reply_markup=markup
    )

def reg_pet(message):
    bot.send_message(message.chat.id, "Введите описание текст объявления")
    bot.register_next_step_handler(message, process_pet_details)

def process_pet_details(message):
    user_pet_data[message.chat.id] = message.text
    markup = types.InlineKeyboardMarkup()
    confirm_btn = types.InlineKeyboardButton("Опубликовать", callback_data='confirm_pet')
    edit_btn = types.InlineKeyboardButton("Изменить", callback_data='edit_pet')
    markup.add(confirm_btn, edit_btn)
    bot.send_message(message.chat.id, f"Проверьте введенные данные:\n\n{message.text}\n\n"
                                      "Выберите опцию:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data in ['confirm_pet', 'edit_pet'])
def confirm_pet_details(call):
    if call.data == 'confirm_pet':
        pet_details = user_pet_data.get(call.message.chat.id)
        if pet_details:
            bot.send_message(channel_charity, pet_details)
            bot.send_message(call.message.chat.id, "Объявление успешно опубликовано!")
        else:
            bot.send_message(call.message.chat.id, "Ошибка.")
    elif call.data == 'edit_pet':
        bot.send_message(call.message.chat.id, "Введите новое объявление.")
        bot.register_next_step_handler(call.message, process_pet_details)

# Handling Мероприятия Section
@bot.message_handler(func=lambda message: message.text in ['Мероприятия', 'Зарегистрировать мероприятие', 'Открыть список мероприятий'])
def handle_events_menu(message):
    if message.text == 'Мероприятия':
        events(message)
    elif message.text == 'Зарегистрировать мероприятие':
        reg_event(message)
    elif message.text == 'Открыть список мероприятий':
        bot.send_message(message.chat.id, "Перейти на канал с мероприятиями: @buddy_events")
    else:
        bot.send_message(message.chat.id, "Повторите попытку.")

def events(message):
    markup = types.ReplyKeyboardMarkup(row_width=1)
    btn1 = types.KeyboardButton('Зарегистрировать мероприятие')
    btn2 = types.KeyboardButton('Открыть список мероприятий')
    btn_back = types.KeyboardButton('Назад')  # "Назад" button
    markup.add(btn1, btn2, btn_back)
    bot.send_message(
        message.chat.id,
        "Выбери подходящую опцию:",
        reply_markup=markup
    )

# Event Registration Section
def reg_event(message):
    try:
        bot.send_message(message.chat.id, "Введите описание мероприятия. Обязательно укажите следующее:\n"
                                          "1) Описание мероприятия\n"
                                          "2) Контакты\n"
                                          "3) Дата, время и место проведения\n"
                                          "4) Ссылки на регистрацию/чаты")
        bot.register_next_step_handler(message, process_event_details)
    except Exception as e:
        bot.send_message(message.chat.id, f"Ошибка: {str(e)}")

def process_event_details(message):
    user_event_data[message.chat.id] = message.text
    markup = types.InlineKeyboardMarkup()
    confirm_btn = types.InlineKeyboardButton("Опубликовать", callback_data='confirm_event')
    edit_btn = types.InlineKeyboardButton("Изменить", callback_data='edit_event')
    markup.add(confirm_btn, edit_btn)
    bot.send_message(message.chat.id, f"Проверьте введенные данные:\n\n{message.text}\n\n"
                                      "Выберите опцию:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data in ['confirm_event', 'edit_event'])
def confirm_event_details(call):
    if call.data == 'confirm_event':
        event_details = user_event_data.get(call.message.chat.id)
        if event_details:
            bot.send_message(channel_events, event_details)
            bot.send_message(call.message.chat.id, "Мероприятие успешно опубликовано!")
        else:
            bot.send_message(call.message.chat.id, "Ошибка: данные о мероприятии не найдены.")
    elif call.data == 'edit_event':
        bot.send_message(call.message.chat.id, "Введите новые данные для мероприятия.")
        bot.register_next_step_handler(call.message, process_event_details)

# Handle "Назад" button
@bot.message_handler(func=lambda message: message.text == 'Назад')
def handle_back_button(message):
    send_welcome(message)

@bot.message_handler(func=lambda message: message.text in ['Психологическая помощь', 'Зарегистрироваться как психолог', 'Найти психолога'])
def handle_psychological_help(message):
    if message.text == 'Психологическая помощь':
        psychological_help_menu(message)
    elif message.text == 'Зарегистрироваться как психолог':
        reg_psychologist(message)
    elif message.text == 'Найти психолога':
        find_psychologist(message)
    else:
        bot.send_message(message.chat.id, "Повторите попытку.")

def psychological_help_menu(message):
    markup = types.ReplyKeyboardMarkup(row_width=1)
    btn1 = types.KeyboardButton('Зарегистрироваться как психолог')
    btn2 = types.KeyboardButton('Найти психолога')
    btn_back = types.KeyboardButton('Назад')  # "Назад" button
    markup.add(btn1, btn2, btn_back)
    bot.send_message(
        message.chat.id,
        "Выбери подходящую опцию:",
        reply_markup=markup
    )

# Psychologist Registration Section
def reg_psychologist(message):
    bot.send_message(message.chat.id, "Введите ваше имя:")
    bot.register_next_step_handler(message, process_psychologist_name)

def process_psychologist_name(message):
    user_id = message.chat.id
    psychologist_data[user_id] = {'name': message.text}
    bot.send_message(message.chat.id, "Введите описание:")
    bot.register_next_step_handler(message, process_psychologist_description)

def process_psychologist_description(message):
    user_id = message.chat.id
    psychologist_data[user_id]['description'] = message.text
    markup = types.ReplyKeyboardMarkup(row_width=1)
    btn_free = types.KeyboardButton('Бесплатно')
    btn_fee = types.KeyboardButton('Платно')
    btn_back = types.KeyboardButton('Назад')  
    markup.add(btn_free, btn_fee, btn_back)
    bot.send_message(message.chat.id, "Укажите, платные услуги или бесплатные:", reply_markup=markup)
    
    bot.register_next_step_handler(message, process_psychologist_fee)

def process_psychologist_fee(message):
    user_id = message.chat.id
    psychologist_data[user_id]['fee'] = message.text
    bot.send_message(message.chat.id, "Введите ваши контакты (номер телефона или Telegram username):")
    bot.register_next_step_handler(message, process_psychologist_contacts)

def process_psychologist_contacts(message):
    user_id = message.chat.id
    psychologist_data[user_id]['contacts'] = message.text
    bot.send_message(message.chat.id, "Вы успешно зарегистрированы как психолог!")

# Find a Psychologist Section
def find_psychologist(message):
    if psychologist_data:
        for user_id, info in psychologist_data.items():
            bot.send_message(
                message.chat.id,
                "Список зарегистрированных психологов:\n"
                f"Имя: {info['name']}\n"
                f"Описание: {info['description']}\n"
                f"Услуги: {info['fee']}\n"
                f"Контакты: {info['contacts']}\n"
            )
        # Add "Назад" button at the end of the psychologist list
    else:
        bot.send_message(message.chat.id, "На данный момент нет зарегистрированных психологов.")
        handle_back_button(message)

# Start the bot
while True:
    try:
        bot.polling(none_stop=True)
    except Exception as e:
        print(f"Error occurred: {e}")
        time.sleep(5)  # Wait for 5 seconds before retrying