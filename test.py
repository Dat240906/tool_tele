import telebot
from telebot import types

bot = telebot.TeleBot('6525705295:AAGaoXer8twK9ZpvUDXyWVclGA3WD6ioH-0')

@bot.message_handler(func=lambda message: message.text == '/start')
def start_command(message):
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton('Thuê BOT tại đây', url='https://t.me/CSKH_VPN4G_BOT'))

    bot.send_message(message.chat.id, 'Chọn hành động:', reply_markup=keyboard)


bot.infinity_polling(timeout=10, long_polling_timeout = 5)