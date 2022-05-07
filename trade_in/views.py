import telebot
import os
import sys
import django

project_path = os.path.dirname(os.path.abspath('../../main.py'))
sys.path.append(project_path)
os.environ["DJANGO_SETTINGS_MODULE"] = "tune.settings"
django.setup()
TOKEN = '5376806714:AAHYWieOq1EM6VYgSI1HmbDE0ttaHVIfMsY'
client = telebot.TeleBot(TOKEN)
path_to_media = 'C:\\Users\\luky\\PycharmProjects\\tune\\media\\'

import trade_in.models as models_trade
from tune_admin.models import Product, Category, SeriesCategory


def get_category():
    result = ['📱 iPhone', '📲 iPad', '💻 MacBook', '🎧 AirPods', '⌚ Watch', '⌨ Устройства']
    return result


def get_series(name_series):
    result = SeriesCategory.objects.filter(category__icontains=f'{name_series}')
    list_1 = []
    for i in result:
        list_1.append(i.category)
    return list_1


def get_detail_product(name_product):
    result = Product.objects.filter(name=f'{name_product}')
    return result


def get_not_category():
    result = Product.objects.all().filter(category_id=6)
    list_device = []
    for r in result:
        list_device.append(r.name)
    return list_device


def get_all_products():
    result = Product.objects.values('name').filter(sell=False).filter(booking=False).filter(moderation=True)
    list_all = []
    for i in result:
        list_all.append(i['name'])
    return list_all


def max_all_products():
    result = Product.objects.values('name')
    list_all = []
    for i in result:
        list_all.append(i['name'])
    return list_all


def get_current_product():
    result = Product.objects.values('series_id').filter(sell=False).filter(booking=False).filter(moderation=True)
    list_id = []
    exit = []
    for i in result:
        list_id.append(i['series_id'])
    for i in list_id:
        result = SeriesCategory.objects.values('category').filter(id=i)
        exit.append(result[0]['category'])
    return list(set(exit))


def get_products(category_name):
    id_category = SeriesCategory.objects.values('id').filter(category__icontains=f'{category_name}')
    result = Product.objects.values('name').filter(series_id=id_category[0]['id']).filter(booking=False).filter(
        sell=False).filter(moderation=True)
    list_product = []
    for i in result:
        list_product.append(i['name'])
    return list_product


def get_price(price_min, price_max):
    result = Product.objects.values('name').filter(price__gte=price_min, price__lte=price_max).filter(
        name__icontains=f'{"iPhone"}').filter(booking=False).filter(sell=False).filter(moderation=True)
    result = [['⋅ ' + str(x['name'])] for x in result]
    print(result)
    return result


def get_max_min_price(cost):
    dia = [[15000, 25000],
           [25000, 35000],
           [35000, 45000],
           [45000, 55000],
           [55000, 70000],
           [70000, 100000]]
    for i in dia:
        if i[0] <= cost <= i[1]:
            return [i[0], i[1]]


def get_sale():
    result = Product.objects.values('name'). \
        filter(sell=False). \
        filter(booking=False). \
        filter(moderation=True). \
        filter(sale=True)
    list_all = []
    for i in result:
        list_all.append(i['name'])
    return list_all


current_category = list(set([x[1] for x in get_current_product()]))
all_products = [x for x in get_all_products()]
current_product = get_current_product()
max_products = [x for x in max_all_products()]


@client.message_handler(func=lambda message: message.text == '⬅️Главное меню')
@client.message_handler(commands=['start'])
def start_message(message, text='Что хотите найти?'):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = telebot.types.KeyboardButton('💥Скидки💥')
    btn2 = telebot.types.KeyboardButton('Новые Устройства')
    btn3 = telebot.types.KeyboardButton('Б/У Устройства')
    btn4 = telebot.types.KeyboardButton('Trade-in / Продажа')
    btn5 = telebot.types.KeyboardButton('Мой бюджет')
    btn6 = telebot.types.KeyboardButton('Устройства с обменки')
    btn7 = telebot.types.KeyboardButton('FAQ')
    btn8 = telebot.types.KeyboardButton('Связаться с менеджером')
    markup.add(btn1)
    markup.add(btn2, btn3)
    markup.add(btn4)
    markup.add(btn5)
    markup.add(btn6, btn7)
    markup.add(btn8)
    client.send_message(message.chat.id, text=text, reply_markup=markup)

from faq.models import FAQModel

faq_info = FAQModel.objects.all()
buttons_info = [['💡 ' + i.name] for i in faq_info]
buttons_info.append(['⬅️Главное меню'])

@client.message_handler(func=lambda message: message.text == 'FAQ')
def main_menu_faq(message, text='Выбирете раздел FAQ'):


    keyboard = telebot.types.ReplyKeyboardMarkup(True, True)
    keyboard.keyboard = buttons_info
    client.send_message(chat_id=message.chat.id,
                        text=text,
                        reply_markup=keyboard)


@client.message_handler(func=lambda message: message.text.split()[0] == '💡')
def main_menu_faq(message, text='Выбирете раздел FAQ'):
    text_message = message.text.replace('💡 ', '')
    info = None
    for i in faq_info:
        if i.name == text_message:
            info = i
            break

    keyboard = telebot.types.ReplyKeyboardMarkup(True, True)
    keyboard.keyboard = buttons_info
    if info.image:
        photo = open(path_to_media + str(info.image), 'rb')
        photo = photo.read()
        client.send_photo(
            chat_id=message.chat.id,
            caption=info.text,
            photo=photo,
            reply_markup=keyboard,
        )
    if not info.image:
        client.send_message(chat_id=message.chat.id,
                            text=info.text,
                            reply_markup=keyboard)




































main_menu = models_trade.TradeInDevicesModel.objects.all()
main_menu = [[buttons.name] for buttons in main_menu]
main_menu.append(['⬅️Главное меню'])
list_user = models_trade.TelegramUserModel.objects.all()
list_user_id = [user_id.user_id for user_id in list_user]


@client.message_handler(func=lambda message: message.text == '⬅️Назад к Trade-in')
@client.message_handler(func=lambda message: message.text == 'Trade-in / Продажа')
def trade_main(message, text='Выберите устройство'):
    id_user = message.chat.id
    if str(id_user) not in list_user_id:
        list_user_id.append(id_user)
        print(list_user_id)
        models_trade.TelegramUserModel.objects.create(
            user_id=id_user,
            username=message.chat.username,
            first_name=message.chat.first_name,
        )

    keyboard = telebot.types.ReplyKeyboardMarkup(True, True)
    keyboard.keyboard = main_menu
    client.send_message(chat_id=message.chat.id,
                        text=text,
                        reply_markup=keyboard)


@client.message_handler(func=lambda message: message.text.split()[0] == '♻️')
def trade_series(message, text='Меню Trade-in'):
    device = message.text.split()[1]
    main_menu_series = models_trade.TradeInSeriesModel.objects.filter(name__icontains=device)
    main_menu_series = [['📍 ' + buttons.name] for buttons in main_menu_series]
    if not main_menu_series:
        trade_main(message=message,
                   text='Этот раздел еще закрыт')
        return 1
    main_menu_series.append(['⬅️Назад к Trade-in'])
    keyboard = telebot.types.ReplyKeyboardMarkup(True, True)
    keyboard.keyboard = main_menu_series
    client.send_message(chat_id=message.chat.id,
                        text='Выберите серию',
                        reply_markup=keyboard)
    models_trade.UserStepModel.objects.filter(
        user__user_id=message.chat.id
    ).delete()


@client.message_handler(func=lambda message: message.text.split()[0] == '📍')
def trade_first_step(message, text='Меню Trade-in'):
    device = message.text.replace('📍 ', '')
    models_trade.UserStepModel.objects.create(
        user=models_trade.TelegramUserModel.objects.filter(user_id=message.chat.id)[0],
        steps_ok='1',
        cost=models_trade.TradeInSeriesModel.objects.filter(name=device)[0].start_cost,
        device=device
    )
    steps = models_trade.TradeInStepModel.objects.filter(series__name=device).filter(step=1)[0]
    steps = models_trade.VariableFoeStepModel.objects.filter(step=steps.id)
    keyboard = telebot.types.ReplyKeyboardMarkup(True, True)
    keyboard.keyboard = [['📌 ' + i.name] for i in steps]
    client.send_message(chat_id=message.chat.id,
                        text=text,
                        reply_markup=keyboard)


@client.message_handler(func=lambda message: message.text.split()[0] == '📌')
def trade_again_step(message, text='Меню Trade-in'):
    user_data = models_trade.UserStepModel.objects.filter(
        user__user_id=message.chat.id,
    )
    device = user_data[0].device
    step = user_data[0].steps_ok
    max_step = models_trade.TradeInSeriesModel.objects.filter(
        name=device
    )[0].max_step
    if int(max_step) != int(step):
        variable = models_trade.VariableFoeStepModel.objects.filter(
            step__step=step,
            name=message.text.replace('📌 ', '')
        )
        new_cost = user_data[0].cost + variable[0].increase - variable[0].decrease
        step = str(int(step) + 1)
        models_trade.UserStepModel.objects.filter(
            user__user_id=message.chat.id,
        ).update(
            steps_ok=step,
            cost=new_cost,
        )
        nex = models_trade.TradeInStepModel.objects.filter(
            step=step,
            series__name=device
        )
        next = models_trade.VariableFoeStepModel.objects.filter(
            step=nex[0].id
        )
        keyboard = telebot.types.ReplyKeyboardMarkup(True, True)
        keyboard.keyboard = [['📌 ' + i.name] for i in next]
        client.send_message(chat_id=message.chat.id,
                            text=text,
                            reply_markup=keyboard)

    else:
        variable = models_trade.VariableFoeStepModel.objects.filter(
            step__step=step,
            name=message.text.replace('📌 ', '')
        )
        new_cost = user_data[0].cost + variable[0].increase - variable[0].decrease
        models_trade.UserStepModel.objects.filter(
            user__user_id=message.chat.id,
        ).update(
            cost=new_cost,
        )
        text = f'Оценка завершина!\n' \
               f'Стоимость {str(new_cost)}'
        trade_main(message=message,
                   text=text)


def get_trade_products():
    result = Product.objects.values('name').filter(
        sell=False,
        booking=False,
        moderation=True,
        state__state='Новое устройство, выдано по гарантии взамен неисправному устройству в авторизованном сервисном центре (АСЦ) Apple. Абсолютно новое, не активированное.'
    )
    list_all = []
    for i in result:
        list_all.append(i['name'])
    return list_all


trade_product = get_trade_products()


@client.message_handler(func=lambda message: message.text == 'Устройства с обменки')
def trade_again_step(message, text='Устрйоства с обмена'):
    tr_products = [['🔁 ' + i] for i in trade_product]
    if not tr_products:
        start_message(message=message,
                      text='В разделе сейчас пусто')
        return 1
    tr_products.append(['⬅️Главное меню'])
    keyboard = telebot.types.ReplyKeyboardMarkup(True, True)
    keyboard.keyboard = tr_products
    client.send_message(chat_id=message.chat.id,
                        text=text,
                        reply_markup=keyboard)


@client.message_handler(func=lambda message: message.text in all_products)
@client.message_handler(func=lambda message: '⋅' in message.text)
@client.message_handler(func=lambda message: message.text.split()[0] == '🔻')
@client.message_handler(func=lambda message: message.text.split()[0] == '🔁')
def show_model(message, extra=None):
    print('Продажа')
    tmp = message.text
    name_to_search = message.text
    name = message.text.split()
    if name[0] == '⋅':
        name.remove('⋅')
    if '⋅' in message.text:
        name_to_search = message.text.replace('⋅ ', '')

    if name[0] == '🔻':
        name.remove('🔻')
    if '🔻' in message.text:
        name_to_search = message.text.replace('🔻 ', '')
    # ----------
    if name[0] == '🔁':
        name.remove('🔁')
    if '🔁' in message.text:
        name_to_search = message.text.replace('🔁 ', '')
    # ----------
    name1 = name[0] + ' ' + name[1][0]
    products = []

    if len(name[1]) > 1 or message.text in get_not_category():

        if message.text in get_not_category():

            products = get_not_category()
        elif (name[1][0] + name[1][1] == 'XR' or name[1][0] + name[1][
            1] == 'SE') and 'watch' not in message.text.lower():

            xr = name[1][0] + name[1][1]
            products = get_products(xr)
        elif name[1][0] in dig and name[1][1] in dig:

            name_11 = name[0] + ' ' + name[1]
            products = get_products(name_11)
        else:
            products = get_products(name1)

    if len(name[1]) == 1 and message.text not in get_not_category():
        products = get_products(name1)

    if message.text in products:
        products.remove(message.text)

    detail_product = get_detail_product(name_to_search)
    if '⋅' in tmp:
        current_price = get_max_min_price(detail_product[0].price)
        products = get_price(current_price[0], current_price[1])
        if [tmp] in products:
            products.remove([tmp])
            products.append(
                ['Забронировать|Узнать подробней' + '\n' + message.text + ' Арт. ' + detail_product[0].article])
        products.append(['⬅️Другой бюджет'])

    elif '🔻' in tmp:
        products = [['🔻 ' + x] for x in get_sale()]
        if [tmp] in products:
            products.remove([tmp])
            products.append(['Забронировать|Узнать подробней' + '\n' + tmp + ' Арт. ' + detail_product[0].article])
        products.append(['⬅️Главное меню'])
    # ----------
    elif '🔁' in tmp:
        products = [['🔁 ' + x] for x in get_trade_products()]
        if [tmp] in products:
            products.remove([tmp])
            products.append(['Забронировать|Узнать подробней' + '\n' + tmp + ' Арт. ' + detail_product[0].article])
        products.append(['⬅️Главное меню'])
    # ----------
    else:
        products = [[x] for x in products]
        products.append(
            ['Забронировать|Узнать подробней' + '\n' + message.text + ' Арт. ' + detail_product[0].article])
        if message.text in get_not_category():
            products.append(['⬅️Назад к Б/У ' + ''])
        else:
            products.append(['⬅️  Назад к Б/У ' + message.text.split()[0]])
    keyboard = telebot.types.ReplyKeyboardMarkup(True, True)
    keyboard.keyboard = products
    if detail_product[0].image_3:
        f1, f2, f3 = open(path_to_media + str(detail_product[0].image_1), 'rb'), \
                     open(path_to_media + str(detail_product[0].image_2), 'rb'), \
                     open(path_to_media + str(detail_product[0].image_3), 'rb')
        f1, f2, f3 = f1.read(), f2.read(), f3.read()
        client.send_media_group(chat_id=message.chat.id, media=[
            telebot.types.InputMediaPhoto(f1, caption=detail_product[0].base_text),
            telebot.types.InputMediaPhoto(f2),
            telebot.types.InputMediaPhoto(f3), ])
        client.send_message(chat_id=message.chat.id,
                            text='Хотите забронировать эту модель?',
                            reply_markup=keyboard)
    else:
        f1, f2 = open(path_to_media + str(detail_product[0].image_1), 'rb'), \
                 open(path_to_media + str(detail_product[0].image_2), 'rb')

        f1, f2 = f1.read(), f2.read()
        client.send_media_group(chat_id=message.chat.id, media=[
            telebot.types.InputMediaPhoto(f1, caption=detail_product[0].base_text),
            telebot.types.InputMediaPhoto(f2)])
        client.send_message(chat_id=message.chat.id,
                            text='Хотите забронировать эту модель?',
                            reply_markup=keyboard)

client.polling(non_stop=True)
