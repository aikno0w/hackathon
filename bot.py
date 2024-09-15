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