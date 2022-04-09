import telebot


# TELEGRAM_URL = 'https://api.telegram.org/bot5239855839:AAGpK1VN7Lr2LDkq0WRC4onTLbYTWyrcc3g'
TOKEN = '5239855839:AAGpK1VN7Lr2LDkq0WRC4onTLbYTWyrcc3g'
URL_BITRIX = 'https://im.bitrix.info/imwebhook/eh/cde3fe41e972cc1f1501bbd0a6d330a11644378495/'
client = telebot.TeleBot(TOKEN)
client.delete_webhook()
# client.set_webhook(url='https://tuneapple.pythonanywhere.com/api')

menu_support = ['-📱 iPhone', '-📲 iPad', '-💻 MacBook',
                '-🎧 AirPods', '-⌚ Watch',
                '-⌨ Устройства', '⬅️Главное меню']

sup_callback = ['Назад к б\у iPhone', 'Назад к б\у  iPad', 'Назад к б\у MacBook',
                'Назад к б\у AirPods', 'Назад к б\у Watch',
                'Назад к б\у Устройства']
