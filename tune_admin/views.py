from ast import literal_eval
from pprint import pprint
import datetime
import telebot
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.exceptions import PermissionDenied
import requests
from .models import Product, Category, SeriesCategory
from cost_models.models import DetailModel
import trade_in.models as models_trade
import trade_id.models as repair_models
from trade_in.models import TelegramUserModel

TOKEN = '5376806714:AAHYWieOq1EM6VYgSI1HmbDE0ttaHVIfMsY'
#
# URL_BITRIX = 'https://im.bitrix.info/imwebhook/eh/6c529968ecadsads581a32c38753edca1c926a16458912ssss57/'
#
client = telebot.TeleBot(TOKEN, threaded=False)
menu_support = ['📱 iPhone', '📲 iPad', '💻 MacBook',
                '🎧 AirPods', '⌚ Watch',
                '⌨ Устройства', '⬅️Главное меню']
sup_callback = ['Назад к Б/У iPhone', 'Назад к Б/У iPad', 'Назад к Б/У MacBook',
                'Назад к Б/У AirPods', 'Назад к Б/У Watch',
                'Назад к Б/У Устройства']

path_to_media = 'C:\\Users\\luky\\PycharmProjects\\tune\\media\\'


@csrf_exempt
def bot(request):
    if request.META['CONTENT_TYPE'] == 'application/json':
        try:

            json_data = request.body.decode('utf-8')
            update = telebot.types.Update.de_json(json_data)
            client.process_new_updates([update])
            print('-----------------------4')
            return HttpResponse({'200': 'ok'})

        except:

            json_data = request.body.decode('utf-8')
            update = telebot.types.Update.de_json(json_data)
            client.process_new_updates([update])
            print('+++++++++++++++++++++++4')
            return HttpResponse({'200': 'ok'})


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
    dia = [[1000, 15000],
           [15000, 25000],
           [25000, 35000],
           [35000, 45000],
           [45000, 55000],
           [55000, 70000],
           [70000, 100000],
           [100000, 130000],
           [130000, 200000], ]
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


sale_tmp = get_sale()

current_category = list(set([x[1] for x in get_current_product()]))
all_products = [x for x in get_all_products()]
current_product = get_current_product()
max_products = [x for x in max_all_products()]


def update_products():
    #     global current_category
    #     global all_products
    #     global current_product
    #     global max_products

    current_category = list(set([x[1] for x in get_current_product()]))
    #     all_products = [x for x in get_all_products()]
    current_product = get_current_product()
    max_products = [x for x in max_all_products()]
    all_products = [x for x in get_all_products()]

main_menu = models_trade.TradeInDevicesModel.objects.all()
main_menu = [[buttons.name] for buttons in main_menu]
main_menu.append(['⬅️Главное меню'])
list_user = models_trade.TelegramUserModel.objects.all()
list_user_id = [int(user_id.user_id) for user_id in list_user]


@client.message_handler(func=lambda message: message.text == 'Запуск')
@client.message_handler(func=lambda message: message.text == 'Начало')
@client.message_handler(func=lambda message: message.text == 'Запустить бота')
@client.message_handler(func=lambda message: message.text == 'Начать')
@client.message_handler(func=lambda message: message.text == 'Старт')
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
    btn9 = telebot.types.KeyboardButton('Ремонт устройств')
    markup.add(btn1)
    markup.add(btn2, btn3)
    markup.add(btn4, btn5)
    markup.add(btn6, btn7)
    markup.add(btn8, btn9)
    client.send_message(message.chat.id, text=text, reply_markup=markup)
    id_user = message.chat.id
    if id_user not in list_user_id:
        list_user_id.append(id_user)
        print(list_user_id)
        models_trade.TelegramUserModel.objects.create(
            user_id=id_user,
            username=message.chat.username,
            first_name=message.chat.first_name,
        )

@client.message_handler(commands=['sm'])
@client.message_handler(func=lambda message: message.text == 'Б/У Устройства')
@client.message_handler(func=lambda message: message.text == '⬅️Назад к Б/У')
def support_menu(message, text='Вот все Б\У'):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = telebot.types.KeyboardButton('📱 iPhone')
    btn2 = telebot.types.KeyboardButton('📲 iPad')
    btn3 = telebot.types.KeyboardButton('💻 MacBook')
    btn4 = telebot.types.KeyboardButton('⌚ Watch')
    btn5 = telebot.types.KeyboardButton('🎧 AirPods')
    btn8 = telebot.types.KeyboardButton('⌨ Устройства')
    btn9 = telebot.types.KeyboardButton('⬅️Главное меню')
    markup.add(btn1)
    markup.add(btn4, btn5)
    markup.add(btn2, btn3)
    markup.add(btn8)
    markup.add(btn9)
    client.send_message(message.chat.id, text=text, reply_markup=markup)


@client.message_handler(func=lambda message: message.text == '⌨ Устройства')
def supp_product(message):
    """
    Обратока для Б\У
    """
    try:
        products = [[x] for x in get_products(message.text.split()[1])]
        products.sort()
        if message.text in get_not_category():
            products.append(['⬅️  Назад к Б/У Устройствам'])
        else:
            products.append(['⬅️Назад к Б/У'])

        keyboard_products = telebot.types.ReplyKeyboardMarkup(True, True)
        keyboard_products.keyboard = products
        client.send_message(chat_id=message.chat.id,
                            text='Ищу: ' + message.text,
                            reply_markup=keyboard_products)
    except:
        support_menu(message, text='В этой категори сейчас пусто😔\n'
                                   'Следите за обнавлениями у нас в канале\n'
                                   'https://t.me/tuneapple 👈')


@client.message_handler(func=lambda message: message.text in menu_support)
@client.message_handler(func=lambda message: " ".join(message.text.split()[1:5]) in sup_callback)
def support_models(message):
    """
    Покажет все модели в наличии
    :param message:
    :return:
    """

    if len(message.text.split()) <= 2:
        model = message.text.split()[1]
    else:
        xxx = message.text.split()
        model = xxx[4]

    models = [x for x in get_series(model) if x in current_product]
    if models == 'iPhone':
        bce = ['iPhone 5', 'iPhone 6 / 6+ / 6s / 6s+',
               'iPhone 7 / 7+', 'iPhone 8 / 8+',
               'iPhone X / XS / XS Max', 'iPhone 11 / Pro / Max',
               'iPhone 12 / Pro / Max / Mini', 'iPhone 13 / Pro / Max / Mini',
               'iPhone SE / XR']

        ect = models.copy()

        models = bce
        x = bce.copy()
        for b in ect:
            if b in x:
                x.remove(b)
        for i in x:
            models.remove(i)

    if models == []:
        support_menu(message, text='В этой категори сейчас пусто😔\n'
                                   'Следите за обнавлениями у нас в канале\n'
                                   'https://t.me/tuneapple 👈')

        return 0

    models = [[x] for x in models]

    models.append(['⬅️Назад к Б/У'])
    keyboard_category = telebot.types.ReplyKeyboardMarkup(True, True)
    keyboard_category.keyboard = models
    client.send_message(chat_id=message.chat.id,
                        text=f'Вот что есть из {model}',
                        reply_markup=keyboard_category)


@client.message_handler(func=lambda message: message.text in current_product)
def support_products(message):
    """
    Отправка клавиатуры наличия моделей по выброной модели/ серии
    :param message:
    :return:
    """
    print(message.chat.id)
    products = [x for x in get_products(message.text)]

    products.sort()
    products = [[x] for x in products]

    if message.text in get_not_category():
        products.append(['⬅️  Назад к Б/У Устройствам'])
    else:
        products.append([f'⬅️  Назад к Б/У {message.text.split()[0]}'])

    keyboard_products = telebot.types.ReplyKeyboardMarkup(True, True)
    keyboard_products.keyboard = products
    client.send_message(chat_id=message.chat.id,
                        text='Ищу: ' + message.text,
                        reply_markup=keyboard_products)


dig = ['1', '2', '3', '4', '5', '6', '7', '8', '9', ]


@client.message_handler(func=lambda message: message.text in all_products)
@client.message_handler(func=lambda message: '⋅' in message.text)
@client.message_handler(func=lambda message: message.text.split()[0] == '🔻')
@client.message_handler(func=lambda message: message.text.split()[0] == '🔁')
def show_model(message, extra=None):
    print('Фото')
    tmp = message.text
    name_to_search = message.text
    try:
        name = message.text.split()
        if name[0] == '⋅':
            name.remove('⋅')
        if '⋅' in message.text:
            name_to_search = message.text.replace('⋅ ', '')

        if name[0] == '🔻':
            name.remove('🔻')
        if '🔻' in message.text:
            name_to_search = message.text.replace('🔻 ', '')

        if name[0] == '🔁':
            name.remove('🔁')
        if '🔁' in message.text:
            name_to_search = message.text.replace('🔁 ', '')

        print('--', name)
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
        print('___+++', name_to_search)
        if '⋅' in tmp:
            current_price = get_max_min_price(detail_product[0].price)
            products = get_price(current_price[0], current_price[1])
            if [tmp] in products:
                products.remove([tmp])
                products.append(
                    ['Забронировать|Узнать подробней' + '\n' + message.text + ' Арт. ' + detail_product[0].article])
            products.append(['⬅️Другой бюджет'])

        elif '🔻' in tmp:
            products = [['🔻 ' + x] for x in sale_tmp]
            if [tmp] in products:
                products.remove([tmp])
                products.append(['Забронировать|Узнать подробней' + '\n' + tmp + ' Арт. ' + detail_product[0].article])
            products.append(['⬅️Главное меню'])

        elif '🔁' in tmp:
            products = [['🔁 ' + x] for x in get_trade_products()]
            if [tmp] in products:
                products.remove([tmp])
                products.append(['Забронировать|Узнать подробней' + '\n' + tmp + ' Арт. ' + detail_product[0].article])
            products.append(['⬅️Главное меню'])

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
    except:
        return 0


@client.message_handler(commands=['nm'])
@client.message_handler(func=lambda message: message.text == 'Новые Устройства')
def new_model(message):
    start_message(message,
                  text='Новые устройства всегда в наличии.\n'
                       'Для заказа выберите пункт «Связаться с менеджером»\n'
                       'Или позвоните по телефону: \n '
                       '+7 (932) 222-54-45')


@client.message_handler(commands=['mb'])
@client.message_handler(func=lambda message: message.text == 'Мой бюджет')
@client.message_handler(func=lambda message: message.text == '⬅️Другой бюджет')
def my_budget(message, text='Выберите бюджет'):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = telebot.types.KeyboardButton('от 1000 до 15000')
    btn2 = telebot.types.KeyboardButton('от 15000 до 25000')
    btn3 = telebot.types.KeyboardButton('от 25000 до 35000')
    btn4 = telebot.types.KeyboardButton('от 45000 до 55000')
    btn5 = telebot.types.KeyboardButton('от 55000 до 70000')
    btn6 = telebot.types.KeyboardButton('от 70000 до 100000')
    btn7 = telebot.types.KeyboardButton('от 100000 до 130000')
    btn8 = telebot.types.KeyboardButton('от 130000 до 200000')
    btn9 = telebot.types.KeyboardButton('⬅️Главное меню')
    markup.add(btn1, btn2)
    markup.add(btn3, btn4)
    markup.add(btn5, btn6)
    markup.add(btn7, btn8)
    markup.add(btn9)
    client.send_message(message.chat.id, text=text, reply_markup=markup)


@client.message_handler(func=lambda message: message.text.split()[0] == 'от')
def my_budget_show(message):
    if len(message.text.split()) >= 4:
        try:
            price_min = message.text.split()[1]
            price_max = message.text.split()[3]
            keyboard_products = get_price(price_min, price_max)

            if keyboard_products == []:
                my_budget(message, 'Ничего не найдено')
                return 0
            keyboard_products.sort()
            keyboard_products.append(['⬅️Другой бюджет'])

            keyboard_category = telebot.types.ReplyKeyboardMarkup(True, True)
            keyboard_category.keyboard = keyboard_products
            client.send_message(chat_id=message.chat.id,
                                text='Вот ссылки на все модели по Вашему бюджету',
                                reply_markup=keyboard_category)
        except:
            pass


# @client.message_handler(commands=['ti'])
# @client.message_handler(func=lambda message: message.text == 'Trade-in / Продажа')
# def tradein_model(message):
#     start_message(message,
#                   text='Программа trade-in доступна!\n'
#                        'С помощью нее вы можете сдать свое старое устройство Apple '
#                        'и получить скидку на новое или б/у (так же принятое по программе trade-in).\n'
#                        'Чтобы узнать размер скидки выберите пункт «Связаться с менеджером»\n '
#                        'Или позвоните по телефону: \n'
#                        '+7 (932) 222-54-45')
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



@client.message_handler(func=lambda message: message.text == '⬅️Назад к Trade-in')
@client.message_handler(func=lambda message: message.text == 'Trade-in / Продажа')
def trade_main(message, text='Выберите устройство'):
    id_user = message.chat.id
    if id_user not in list_user_id:
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


@client.message_handler(commands=['sale'])
@client.message_handler(func=lambda message: message.text == '💥Скидки💥')
def tradein_model(message):
    sale = get_sale()
    result = [['🔻 ' + x] for x in sorted(sale)]
    result.append(['⬅️Главное меню'])
    keyboard_products = telebot.types.ReplyKeyboardMarkup(True, True)
    keyboard_products.keyboard = result
    client.send_message(chat_id=message.chat.id,
                        text='Вот все скидки',
                        reply_markup=keyboard_products)


@client.message_handler(func=lambda message: message.text == 'Ремонт устройств')
def main_menu_repair(message, text='Выбирите устройство'):
    try:
        repair_models.UserChoiceModel.objects.filter(
            user_id=TelegramUserModel.objects.get(
                user_id=message.chat.id
            ).id
        ).delete()
    except:
        pass


    buttons = repair_models.ButtonModel.objects.all()
    buttons = [['🔧 ' + i.name_button] for i in buttons]
    buttons.append(['⬅️Главное меню'])
    keyboard_products = telebot.types.ReplyKeyboardMarkup(True, True)
    keyboard_products.keyboard = buttons
    client.send_message(chat_id=message.chat.id,
                        text=text,
                        reply_markup=keyboard_products)


@client.message_handler(func=lambda message: message.text.split()[0] == '🔧')
def service_repair(message):
    device = message.text.replace('🔧 ', '')
    id_user = TelegramUserModel.objects.get(
        user_id=message.chat.id
    ).id
    user_device = repair_models.UserChoiceModel.objects.filter(
        user_id=id_user
    )
    if not user_device:
        user_query = TelegramUserModel.objects.get(
            user_id=message.chat.id,
        )
        user_device = repair_models.UserChoiceModel.objects.create(
            user_id=user_query,
            cost=0,
            device=device
        )
        buttons = repair_models.ServiceModels.objects.filter(
            series__name_button=message.text.replace('🔧 ', '')
        )
        buttons = [['Завершить и показать сумму ремонта']] + [['🔧 ' + i.name] for i in buttons]
        buttons.append(['⬅️Главное меню'])
        keyboard_products = telebot.types.ReplyKeyboardMarkup(True, True)
        keyboard_products.keyboard = buttons
        client.send_message(chat_id=message.chat.id,
                            text='text',
                            reply_markup=keyboard_products)
        return 1

    else:
        user_cost = user_device[0].cost
        user_device = user_device[0].device
        up = repair_models.ServiceModels.objects.filter(
            series__name_button=user_device,
            name=device
        )

        buttons = repair_models.ButtonModel.objects.get(
            name_button=user_device
        )
        buttons = repair_models.ServiceModels.objects.filter(
            series=buttons
        )
        id_user = TelegramUserModel.objects.get(
            user_id=message.chat.id
        )
        id_user = repair_models.UserChoiceModel.objects.get(
            user_id=id_user
        )
        xx = repair_models.UseService.objects.filter(
            user=id_user,
        )
        if message.text in [i.name_service for i in xx]:
            pass
        else:
            repair_models.UseService.objects.create(
                user=id_user,
                name_service=message.text
            )
            repair_models.UserChoiceModel.objects.update(
                device=user_device,
                cost=str(int(user_cost) + int(up[0].cost))
            )
        buttons = [['Завершить и показать сумму ремонта']] + [['🔧 ' + i.name] for i in buttons]
        buttons.append(['⬅️Главное меню'])
        keyboard_products = telebot.types.ReplyKeyboardMarkup(True, True)
        keyboard_products.keyboard = buttons
        client.send_message(chat_id=message.chat.id,
                            text=f'{message.text.replace("🔧 ", "")}'
                                 f'\n\n'
                                 f'Услуга успешно добавлена',
                            reply_markup=keyboard_products)


@client.message_handler(func=lambda message: message.text == 'Завершить и показать сумму ремонта')
def service_repair_exit(message):
    services = repair_models.UseService.objects.filter(
        user_id=repair_models.UserChoiceModel.objects.filter(
            user_id=TelegramUserModel.objects.get(
                user_id=message.chat.id
            ).id
        )[0].id
    )
    cost = repair_models.UserChoiceModel.objects.filter(
        user_id=TelegramUserModel.objects.get(
            user_id=message.chat.id
        ).id
    )[0].cost
    print(cost)
    text = "".join([' -- ' + i.name_service.replace("🔧 ", "")
                    + '\n' for i in services])
    text = 'Выбраные услуги: \n' + text
    text = text + f'\nИтоговая стоимость:\n{str(cost)} рублей'

    start_message(
        message=message,
        text=text
    )


# @client.message_handler(content_types=['text'])
# def bitrix_client(message):
#     if message.text not in max_products:
#         if message.text.split()[0] != 'Бюджет':
#             try:
#                 print('---', message.text)
#                 jsn = message.__dict__.get('json')
#
#                 ts = {'update_id': 287246100,
#                       'message': {'message_id': jsn['message_id'],
#                                   'from': {'id': jsn['from']['id'],
#                                            'is_bot': False,
#                                            'first_name': jsn['from']['first_name'],
#                                            'language_code': jsn['from']['language_code']},
#                                   'chat': {'id': jsn['chat']['id'],
#                                            'first_name': jsn['chat']['first_name'],
#                                            'type': jsn['chat']['type']},
#                                   'date': jsn['date'],
#                                   'text': jsn['text']}}
#
#                 requests.post(URL_BITRIX, json=ts)
#
#                 if message.text.lower().split()[0] == 'забронировать|узнать' or \
#                         message.text.lower() == 'купить новое устройство':
#                     start_message(message, text='Пожалуйста дождитесь ответа менеджера,'
#                                                 ' он поможет Вам забронировать устройство или расскажет о нем более подробно 👩🏻‍💻')
#                     start_message(message,
#                                   text='Сейчас наблюдаются сбои в работе телеграмма, если менеджер не отвечает, пожалуйста, свяжитесь с нами по телефону\n +7 (932) 222-54-45')
#                 if message.text.lower() == 'связаться с менеджером':
#                     start_message(message, text='Через несколько минут с Вами свяжется менеджер\n'
#                                                 'Пожалуйста, ожидайте')
#                     start_message(message,
#                                   text='Сейчас наблюдаются сбои в работе телеграмма, если менеджер не отвечает, пожалуйста, свяжитесь с нами по телефону\n +7 (932) 222-54-45')
#             except Exception as _:
#                 try:
#                     jsn = message.__dict__.get('json')
#                     ts = {'update_id': 287246100,
#                           'message': {'message_id': jsn['message_id'],
#                                       'from': {'id': jsn['from']['id'],
#                                                'is_bot': False,
#                                                'first_name': jsn['from']['first_name'],
#                                                'language_code': jsn['from']['language_code']},
#                                       'chat': {'id': jsn['chat']['id'],
#                                                'first_name': jsn['chat']['first_name'],
#                                                'type': jsn['chat']['type']},
#                                       'date': jsn['date'],
#                                       'text': jsn['text']}}
#
#                     requests.post(URL_BITRIX, json=ts)
#                     start_message(message, text='Я вас не понимаю 🙄\n'
#                                                 'Напишите еще раз')
#                 except:
#                     start_message(message, text='Произошла ошибка телеграмма 🙄\n'
#                                                 'Попробуйте написать через 5 минут'
#                                                 'Или напишите нашему менеджеру — Виктории @VasViktory')
#
#
# @client.message_handler(content_types=['photo'])
# def photo(message):
#     jsn = message.__dict__.get('json')
#     exit_dict = {"update_id": 287246100} | {"message": jsn}
#     requests.post(URL_BITRIX, json=exit_dict)

client.polling(non_stop=True)
