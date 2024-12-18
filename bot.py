import telebot
import smtplib
import re


# Теперь загрузите переменные
BOT_TOKEN = '7288594127:AAHZ02odv_TaukTndvvO5lP9Eb8dZ2zh0Kk'
EMAIL_LOGIN = 'Vasilecnastya03@yandex.ru'
EMAIL_PASSWORD = 'qxrcetlxnkaznciq'

print("BOT_TOKEN:", BOT_TOKEN)
print("EMAIL_LOGIN:", EMAIL_LOGIN)
print("EMAIL_PASSWORD:", EMAIL_PASSWORD)

EMAIL_PATTERN = re.compile(r'[0-9a-zA-Z]+@[0-9a-zA-Z]+\.[0-9a-zA-Z]+')

SMTP_HOST = 'smtp.yandex.ru'
SMTP_PORT = 587

def send_message(destination: str, text: str) -> tuple[str, bool]:
    try:
        server = smtplib.SMTP(SMTP_HOST, SMTP_PORT)
        server.ehlo()
        server.starttls()
        server.login(EMAIL_LOGIN, EMAIL_PASSWORD)
    except Exception as ex:
        return f"Can't initialize SMTP server - {ex.__str__()}", False

    try:
        message = f'''
        From: {EMAIL_LOGIN}
        To: {destination}
        Subject: Telegram Bot message

        {text}'''  
        server.sendmail(EMAIL_LOGIN, destination, message.encode('utf-8'))
    except Exception as ex:
        return f'При отправке сообщения возникла ошибка - {ex.__str__()}', False
    else:
        return 'Сообщение успешно отправлено', True
    finally:
        server.quit()

destination = ''
waiting_for_message = False

# Проверка на наличие токена
if BOT_TOKEN is None:
    raise ValueError("BOT_TOKEN не установлен.")

bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def ask_email(message):
    bot.send_message(message.chat.id, 'Напишите свой email')

@bot.message_handler()
def handle_email(message):
    global destination
    global waiting_for_message

    successful = False

    if EMAIL_PATTERN.match(message.text):
        reply = 'Email написан правильно. Введите текст сообщения'
        destination = message.text
        waiting_for_message = True
    else:
        if waiting_for_message:
            reply, successful = send_message(destination, message.text)
        else:
            reply = 'Неправильный формат Email'

    bot.reply_to(message, reply)
    if successful:
        ask_email(message)
        destination = ''
        waiting_for_message = False

bot.infinity_polling()
