import telebot
import requests
TOKEN = '6884166250:AAGWagRUVWsPBmvxApwcA36ZZ2zCYs1yDRI'

bot = telebot.TeleBot(TOKEN)

commands = """
<u>CÁC LỆNH:</u>
<b>
/get2fa [secret_key]
/uid [link]
</b>
"""


def get_2fa(secret_key):
    api_web_get = f'https://2fa.live/tok/{secret_key}'
    response = requests.get(api_web_get)

    data = response.json()
    if data:
        code = data['token']
        return code
    return None

def get_UID_from_link(link):
    url = f"https://fbuid.mktsoftware.net/api/v1/fbprofile?url={link}"

    response = requests.get(url)
    data = response.json()    

    if not data:
        return None 
    return data['uid']

    

@bot.message_handler(func=lambda message: True)
def echo_message(message):
    content = message.text.lower()

    if content.startswith('/get2fa') and len(content.split()) == 2:
        secret_key = content.split()[1]
        code = get_2fa(secret_key)
        if code:
            return bot.reply_to(message, f"<b>{code}</b>", parse_mode = 'html')
        return bot.reply_to(message, f"<b>API get2fa có lỗi!</b>")
    if content.startswith('/uid') and len(content.split()) == 2:
        link = content.split()[1]
        uid = get_UID_from_link(link)
        if uid:
            return bot.reply_to(message, f"<b>{uid}</b>", parse_mode = 'html')
        return bot.reply_to(message, f"<b>API getuid có lỗi!</b>")
    if content.startswith("/help"):
        bot.reply_to(message, commands, parse_mode = 'html')

bot.infinity_polling(timeout=10, long_polling_timeout = 5)