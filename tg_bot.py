import telebot
from telebot import types
from config import TOKEN, MY_CHAT_ID

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start_message(message):
    user_name = message.from_user.first_name
    
    keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    keyboard.add(
        types.KeyboardButton(text='📋 Услуги'),
        types.KeyboardButton(text='🏢 О нас'),
        types.KeyboardButton(text='✍️ Оставить заявку')
    )

    bot.send_message(
        message.chat.id, f'Здравствуйте, {user_name}! 👋\n\nЯ ваш виртуальный консультант. Выберите нужный раздел в меню ниже.', 
        reply_markup=keyboard
    )


def info_func(message):
    keyboard = types.InlineKeyboardMarkup()
    url_button = types.InlineKeyboardButton(text='🌐 Перейти на наш сайт', url='https://ya.ru')
    keyboard.add(url_button)
    
    about_text = (
        "🏢 О нашей компании\n\n"
        "Мы предоставляем профессиональные финансовые услуги для бизнеса. "
        "Работаем честно, быстро и надежно.\n\n"
        "Узнайте больше на нашем сайте:"
    )
    bot.send_message(message.chat.id, about_text, reply_markup=keyboard)


def get_service(message):
    service_name = message.text
    
    bot.send_message(
        message.chat.id, 
        'Отлично! Теперь напишите ваше имя и телефон (например: Иван, +7 999 123-45-67).'
    )
    
    bot.register_next_step_handler(message, lambda msg: send_request(msg, service_name))


def send_request(message, service_name):
    contacts = message.text
    
    admin_message = f'🔔 Новая заявка!\n🛠 Услуга: {service_name}\n👤 Контакты: {contacts}'
    bot.send_message(MY_CHAT_ID, admin_message)
    
    bot.send_message(
        message.chat.id, 
        '✅ Заявка отправлена! Мы скоро свяжемся с вами.'
    )

def send_service(message):
    services_text = (
        "📋 **Наши услуги:**\n\n"
        "📊 Составление годовой отчетности\n"
        "💳 Оптимизация и оплата налогов\n"
        "📈 Расчет бизнес-бюджета"
    )
    bot.send_message(message.chat.id, services_text, parse_mode='Markdown')


@bot.message_handler(content_types=['text'])
def handle_text_messages(message):
    user_text = message.text.strip().lower()
    
    if user_text == '🏢 о нас':
        info_func(message)
        
    elif user_text == '✍️ оставить заявку':
        bot.send_message(
            message.chat.id, 'Отличный выбор! 🤝\nНапишите, какая услуга вас интересует (например: Расчет бизнес-бюджета).'
        )
        bot.register_next_step_handler(message, get_service)
        
    elif user_text == '📋 услуги':
        send_service(message)
        
    else:
        bot.send_message(
            message.chat.id, 
            'Я вас не понял. 🤖 Пожалуйста, используйте кнопки меню ниже:',
            reply_markup=types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True).add(
                types.KeyboardButton(text='📋 Услуги'),
                types.KeyboardButton(text='🏢 О нас'),
                types.KeyboardButton(text='✍️ Оставить заявку')
            )
        )

if __name__ == '__main__':
    print("✅ Бот запущен!")
    bot.infinity_polling()