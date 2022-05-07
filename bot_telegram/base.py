# import telebot


# TELEGRAM_URL = 'https://api.telegram.org/bot5239855839:AAGpK1VN7Lr2LDkq0WRC4onTLbYTWyrcc3g'
# TOKEN = '5239855839:AAGMSUsbode-6PO_sOwVlqPmr6XsoAHfhY4'
# TOKEN = '5239855839:AAGMSUsbode-6PO_sOwVlqPmr6XsoAHfhY4'
# # URL_BITRIX = 'https://im.bitrix.info/imwebhook/eh/cde3fe41e972cc1f1501bbd0a6d330a11644378495/'
# client = telebot.TeleBot(TOKEN, threaded=False)
# client.delete_webhook()
# client.set_webhook(url='https://tuneapple.xyz/api/v1')
# client.set_webhook(url='https://TuneApple.pythonanywhere.com/panel/b')
# menu_support = ['-📱 iPhone', '-📲 iPad', '-💻 MacBook',
#                 '-🎧 AirPods', '-⌚ Watch',
#                 '-⌨ Устройства', '⬅️Главное меню']

# sup_callback = ['Назад к б\у iPhone', 'Назад к б\у  iPad', 'Назад к б\у MacBook',
#                 'Назад к б\у AirPods', 'Назад к б\у Watch',
#                 'Назад к б\у Устройства']
#
# import io
# import requests
# from PIL import Image
#
# username = 'TuneApple'
# token = 'd1cfd6bbfc894c3592932df061dd238d291fb5e3'
# domain_name = 'TuneApple.pythonanywhere.com'
#
# def restart_server():
#     response = requests.get(
#             'https://www.pythonanywhere.com/api/v0/user/{username}/files/path{path}'.format(
#             username=username,
#             path='/home/TuneApple/tune/media'
#         ),
#         headers={'Authorization': 'Token {token}'.format(token=token)}
#     )
#     return response.json()
#
# result = restart_server()
#
# keys = [i for i in result]
# links_image = []
# for link in keys:
#     s = result[link]['url']
#     links_image.append(s)
#
# for i in links_image:
#     response = requests.get(
#         i,
#         headers={'Authorization': 'Token {token}'.format(token=token)}
#     )
#     con = response.content
#     image = Image.open(io.BytesIO(con))
#     # image = Image.frombytes('RGBA', (128,128), con)
#     name = i.split('/')[-1]
#     image.save("/home/apple/code/project1/tune/media/" + name)
#     print(name)

# import os
#
# os.system('sudo supervisorctl status gunicorn | sed "s/.*[pid ]\([0-9]\+\)\,.*/\1/" | xargs kill -HUP')
# print("`cd ~` ran with exit code %d" % home_dir)
# unknown_dir = os.system("cd doesnotexist")
# print("`cd doesnotexis` ran with exit code %d" % unknown_dir)
# import subprocess
#
# list_files = subprocess.run(["ls"])
# print("The exit code was: %d" % list_files.returncode)
# import datetime
#
# import telebot
# import os
# import sys
# import django
# from django.contrib.auth import get_user_model
#
# today = datetime.date.today()
# tomorrow = today + datetime.timedelta(days=4)
#
# project_path = os.path.dirname(os.path.abspath('../../main.py'))
# sys.path.append(project_path)
# os.environ["DJANGO_SETTINGS_MODULE"] = "tune.settings"
# django.setup()
# from tune_admin.models import Product, StateModel, GuarantyModel, KitModel, Category, SeriesCategory
# x = get_user_model()
#
#
# TOKEN = '5376806714:AAFzE6HW2XfZl_AlvzHKO2vsbcfsT6Eg3k8'
# bot = telebot.TeleBot(TOKEN)
# first_parking = Product.objects.all()
# prod = Product.objects.create(
#                 image_1='photo1643559946_3.jpeg',
#                 image_2='photo1643559946_4.jpeg',
#                 image_3='photo1643559946_5.jpeg',
#                 sell=False,
#                 booking=False,
#                 moderation=False,
#                 price='31000',
#                 smile='₽',
#                 name='iPhone 8 256 Gold - 33.990₽',
#                 name_tmp='iPhone 8 256 Gold',
#                 tests=False,
#                 article='4363522',
#                 state=StateModel.objects.get(id=1),
#                 state_akb='22',
#                 works=None,
#                 kit=KitModel.objects.get(id=1),
#                 guaranty=GuarantyModel.objects.get(id=1),
#                 custom_guaranty=None,
#                 base_text='Базовый текст',
#                 day_created=datetime.datetime.today(),
#                 category=Category.objects.get(id=1),
#                 series=SeriesCategory.objects.get(id=1),
#                 author=x.objects.get(id=1),
#                 count='1',
#                 up_price=False,
#                 provider_device='Устройсво клиента',
#                 device_provider='0',
#
#             )
# print(prod.id)
#
# import re
# memory = '32|64|128|256|512'
# memory_iphone = re.findall(memory, prod.name_tmp)
# dict_avito = {
#     'Id': prod.id,
#     'AvitoId': None,
#     'AdStatus': 'Free',
#     'Category': 'Телефоны',
#     'GoodsType': 'iPhone',
#     'Address': 'Самовывоз - СПБ, ул. Восстания 7, БЦ «Андреевский», офис 208',
#     'Title': prod.name_tmp,
#     'Description': 'иекси',  #prod.base_text
#     'Condition': 'Состояние',
#     'Price': prod.price,
#     'DateBegin': '',
#     'DateEnd': '',
#     'AllowEmail': 'lindel33@mail.ru',
#     'ManagerName': 'TuneApple',
#     'ContactPhone': '89995309522',
#     'Brand': 'Apple',
#     'Model': '13 Pro Max',
#     'Color': 'Цвет',
#     'MemorySize': memory_iphone,
#     'RamSize': '',
#     'ImageUrls': str(prod.image_1) + '|' + str(prod.image_2)
# }
# from avito import new_avito
# new_avito(dict_avito)
# """
#     'DateBegin':,
#     'DateEnd':,
#     'RamSize': ,
#
# """
#
# new = Product.objects.filter(id=prod.id).delete()



















#
# @bot.message_handler(commands=['start'])
# def send_welcome(message):
#     for i in first_parking:
#         bot.send_message(message.chat.id, i)
#
#
# bot.polling(none_stop=True)
#
