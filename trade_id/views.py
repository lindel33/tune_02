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
import trade_id.models as repair_models
from trade_in.models import TelegramUserModel


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


@client.message_handler(func=lambda message: message.text == 'Ремонт устройств')
def main_menu_repair(message, text='Выбирите устройство'):
    repair_models.UserChoiceModel.objects.filter(
        user_id=TelegramUserModel.objects.get(
            user_id=message.chat.id
        ).id
    ).delete()

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


# client.polling(non_stop=True)
