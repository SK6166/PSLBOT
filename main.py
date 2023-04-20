import telebot
import background
import pymorphy2
import sqlite3
import time
import openai
import pytz
import websockets
import asyncio
import base64
import json
from datetime import datetime

from random import randint
from telebot import types

# -----------------------------------------------------------------------------------------------------------------------
openai.api_key = "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"

engine = "text-davinci-003"

# -----------------------------------------------------------------------------------------------------------------------
background.keep_alive()

bot = telebot.TeleBot('6042579739:AAGWGSwQTS_lVmWME8Qe5A5m6e7tH3HeXu0')

comandslist = ['start', 'restart', ['prediction']]

fa = {
    'море': 'вас что-то волнует',
    'солнце': 'Близятся перемены',
    'сонечный': 'Счастье',
    'луна': 'Спокойствие',
    'день': 'однотипность',
    'ветер': 'беспокойствие',
    'дом': 'уют',
    'друзья': 'Вы попали в ситуацию, самостоятельно выбраться из которой вам будет не под силу',
    'друг': 'Вы попали в ситуацию, самостоятельно выбраться из которой вам будет не под силу',
    'подруга': 'Вы попали в ситуацию, самостоятельно выбраться из которой вам будет не под силу',
    'пальма': 'отдых',
    'рыба': 'изменение в жизни',
    'интел': 'процессор',
    'работа': 'вы замкнуты в себе',
}

p = ['Удача благовалит вам', 'Стремитесь к успеху и выглядите так, словно вы его уже достигли.',
     'ичего не может быть смешнее, чем нравиться всем и каждому.',
     'Каждый дарованный нам день является первым в том отрезке жизни, что нам остался.',
     'Стоя на месте, двигаться можно только назад.',
     'Нужно делать то, что ты должен делать. И пусть все будет так, как будет.',
     'Разница между победителем и побежденным только в том, что первый поднялся больше раз, чем упал.',
     'Лучше сделать и пожалеть о сделанном, чем не сделать и сожалеть о не сделанном.',
     'Слушайте каждого. Идеи приходят отовсюду.', 'Уделите особое внимание старой дружбе.',
     'Терпение! Вы почти у цели.', 'Романтика переместит вас в новом направлении.',
     'Пришло время закончить старое и начать новое.', 'Поздравляем! Вы находитесь на верном пути.',
     'Кто-то нуждается в вашей поддержке', 'Вам предстоит рассмотреть неожиданное предложение',
     'Не оставляйте усилий и получите желаемое']

lid = 8

lday = '26.03.2023'


def find_ans(text):
    # Запрос
    prompt = f"Раскажи что значит мой сон:\n{text}"

    # Модель
    completion = openai.Completion.create(engine=engine,
                                          prompt=prompt,
                                          temperature=0.4,
                                          max_tokens=1000)

    return completion.choices[0]['text'].split('\n')[-1]


# morph = pymorphy2.MorphAnalyzer()
#   s = text.split()
#  res = []
# for i in s:
#    p = morph.parse(i)[0]
#   res.append((i.lower(), p.normal_form))
#    itogo = []
#   for i in res:
#      a = i[1]
#     if a in fa:
#        znach = fa[a]
#       itogo.append(f'{a} - {znach}')
#  if '\n'.join(itogo) == '':
#     return 'Не удалось расшифровать сон'
# return '\n'.join(itogo)


def predskazanie():
    utcmoment_naive = datetime.utcnow()
    utcmoment = utcmoment_naive.replace(tzinfo=pytz.utc)
    localFormat = "%Y-%m-%d"

    timezone = 'Europe/Saratov'
    localDatetime = utcmoment.astimezone(pytz.timezone(timezone))
    print(localDatetime.strftime("%Y-%m-%d %H:%M:%S"))

    global lid, lday
    k = lid
    day = lday
    if localDatetime.strftime(localFormat) == day:
        s = p[lid]
    else:
        while k == lid:
            lid = randint(0, 17)
        s = p[lid]
        lday = localDatetime.strftime(localFormat)
    return s


@bot.message_handler(commands=['start', 'restart'])
def start(message):
    bot.send_message(message.from_user.id,
                     f"""Привет {message.from_user.first_name} я PSLeep бот.
Напиши мне свой сон а я дам значаение.
Напишите /prediction если хотите узнать предсказание на сегодня
Напишите /compatibility если хотите узнать совместимость двух людей""",
                     reply_markup=types.ReplyKeyboardRemove())


@bot.message_handler(commands=['prediction'])
def pred(message):
    bot.send_message(message.from_user.id, f'''Предсказание на сегодня:
{predskazanie()}''', reply_markup=types.ReplyKeyboardRemove())
    bot.send_message(message.from_user.id,
                     f"""Напиши мне свой сон а я дам значаение.
    Напишите /prediction если хотите узнать предсказание на сегодня
    Напишите /compatibility если хотите узнать совместимость двух людей""",
                     reply_markup=types.ReplyKeyboardRemove())


@bot.message_handler(commands=['compatibility'])
def compatibility1(message, k=0):
    user_list1 = {'znak': None, 'pol': None, 'age': None}
    user_list2 = {'znak': None, 'pol': None, 'age': None}
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
    btn1 = types.KeyboardButton(text="""Овен\n♈""")
    btn2 = types.KeyboardButton(text="Телец\n♉")
    btn3 = types.KeyboardButton(text="Близнецы\n♊")
    btn4 = types.KeyboardButton(text="Рак\n♋")
    btn5 = types.KeyboardButton(text="Лев\n♌")
    btn6 = types.KeyboardButton(text="Дева\n♍")
    btn7 = types.KeyboardButton(text="Весы\n♎")
    btn8 = types.KeyboardButton(text="Скорпион\n♏")
    btn9 = types.KeyboardButton(text="Стрелец\n♐")
    btn10 = types.KeyboardButton(text="Козерог\n♑")
    btn11 = types.KeyboardButton(text="Водолей\n♒")
    btn12 = types.KeyboardButton(text="Рыбы\n♓")
    markup.add(btn1, btn2, btn3, btn4, btn5, btn6, btn7, btn8, btn9, btn10, btn11, btn12)
    if k == 0:
        bot.send_message(message.from_user.id, f'''Выберете знак зодиака первого человека:''', reply_markup=markup)
    if message.text in ["Рыбы\n♓", "Водолей\n♒", "Козерог\n♑", "Стрелец\n♐", "Скорпион\n♏", "Весы\n♎", "Дева\n♍",
                        "Лев\n♌",
                        "Рак\n♋",
                        "Близнецы\n♊", "Телец\n♉", "Овен\n♈"]:
        compatibility2(message, user_list1, user_list2, a=['znak'])
    else:
        if k != 0:
            bot.send_message(message.chat.id, f'''Неправильный знак зодиака, попробуйте еще раз''',
                             reply_markup=markup)
        if k == 0:
            k += 1
        bot.register_next_step_handler(message,
                                       compatibility1,
                                       k=k)


def compatibility2(message, user_list1, user_list2, k=0, a=None):
    if a == ['znak']:
        user_list1['znak'] = message.text
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn1 = '♂Мужской♂'
    btn2 = '♀Женский♀'
    markup.add(btn1, btn2)
    if k == 0:
        bot.send_message(message.from_user.id, 'Выберете пол первого человека:', reply_markup=markup)
    if message.text in ['♂Мужской♂', '♀Женский♀']:
        compatibility3(message, user_list1, user_list2, a='pol')
    else:
        if k != 0:
            bot.send_message(message.from_user.id, f'''Неправильный пол, попробуйте еще раз''',
                             reply_markup=markup)
        if k == 0:
            k += 1
        bot.register_next_step_handler(message, compatibility2, user_list1, user_list2, k=k)


def compatibility3(message, user_list1, user_list2, k=0, a=None):
    if a == 'pol':
        user_list1['pol'] = message.text
    if k == 0:
        bot.send_message(message.from_user.id, 'Введите возраст первого человека:',
                         reply_markup=types.ReplyKeyboardRemove())
    if message.text in list(map(str, range(0, 999))):
        compatibility4(message, user_list1, user_list2, a='age')
    else:
        if k != 0:
            bot.send_message(message.from_user.id, f'''Неправильный возраст(1 - 100), попробуйте еще раз''',
                             reply_markup=types.ReplyKeyboardRemove())
        if k == 0:
            k += 1
        bot.register_next_step_handler(message, compatibility3, user_list1, user_list2, k=k)


def compatibility4(message, user_list1, user_list2, k=0, a=None):
    if a == 'age':
        user_list1['age'] = message.text
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
    btn1 = types.KeyboardButton(text="""Овен\n♈""")
    btn2 = types.KeyboardButton(text="Телец\n♉")
    btn3 = types.KeyboardButton(text="Близнецы\n♊")
    btn4 = types.KeyboardButton(text="Рак\n♋")
    btn5 = types.KeyboardButton(text="Лев\n♌")
    btn6 = types.KeyboardButton(text="Дева\n♍")
    btn7 = types.KeyboardButton(text="Весы\n♎")
    btn8 = types.KeyboardButton(text="Скорпион\n♏")
    btn9 = types.KeyboardButton(text="Стрелец\n♐")
    btn10 = types.KeyboardButton(text="Козерог\n♑")
    btn11 = types.KeyboardButton(text="Водолей\n♒")
    btn12 = types.KeyboardButton(text="Рыбы\n♓")
    markup.add(btn1, btn2, btn3, btn4, btn5, btn6, btn7, btn8, btn9, btn10, btn11, btn12)
    if k == 0:
        bot.send_message(message.from_user.id, f'''Выберете знак зодиака второго человека:''', reply_markup=markup)
    if message.text in ["Рыбы\n♓", "Водолей\n♒", "Козерог\n♑", "Стрелец\n♐", "Скорпион\n♏", "Весы\n♎", "Дева\n♍",
                        "Лев\n♌",
                        "Рак\n♋",
                        "Близнецы\n♊", "Телец\n♉", "Овен\n♈"]:
        compatibility5(message, user_list1, user_list2, a='znak')
    else:
        if k != 0:
            bot.send_message(message.chat.id, f'''Неправильный знак зодиака, попробуйте еще раз''',
                             reply_markup=markup)
        if k == 0:
            k += 1
        bot.register_next_step_handler(message,
                                       compatibility4,
                                       user_list1, user_list2,
                                       k=k)


def compatibility5(message, user_list1, user_list2, k=0, a=None):
    if a == 'znak':
        user_list2['znak'] = message.text
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn1 = '♂Мужской♂'
    btn2 = '♀Женский♀'
    markup.add(btn1, btn2)
    if k == 0:
        bot.send_message(message.from_user.id, 'Выберете пол второго человека:', reply_markup=markup)
    if message.text in ['♂Мужской♂', '♀Женский♀']:
        compatibility6(message, user_list1, user_list2, a='pol')
    else:
        if k != 0:
            bot.send_message(message.from_user.id, f'''Неправильный пол, попробуйте еще раз''',
                             reply_markup=markup)
        if k == 0:
            k += 1
        bot.register_next_step_handler(message, compatibility5, user_list1, user_list2, k=k)


def compatibility6(message, user_list1, user_list2, k=0, a=None):
    if a == 'pol':
        user_list2['pol'] = message.text
    if k == 0:
        bot.send_message(message.from_user.id, 'Введите возраст второго человека(1 - 100):',
                         reply_markup=types.ReplyKeyboardRemove())
    if message.text in list(map(str, range(0, 999))):
        done(message, user_list1, user_list2, a='age')
    else:
        if k != 0:
            bot.send_message(message.from_user.id, f'''Неправильный возраст(1 - 100), попробуйте еще раз''',
                             reply_markup=types.ReplyKeyboardRemove())
        if k == 0:
            k += 1
        bot.register_next_step_handler(message, compatibility6, user_list1, user_list2, k=k)


def done(message, user_list1, user_list2, a=None):
    if a == 'age':
        user_list2['age'] = message.text
    z1 = ' '.join(user_list1['znak'].split("\n"))
    z2 = ' '.join(user_list2['znak'].split("\n"))
    bot.send_message(message.from_user.id, f'''Вычисляю cовместимость:
---------------
Знак - {z1}
Пол - {user_list1['pol']}
Возраст - {user_list1['age']}
---------------
И
---------------
Знак - {z2}
Пол - {user_list2['pol']}
Возраст - {user_list2['age']}
---------------''', reply_markup=types.ReplyKeyboardRemove())
    bot.send_message(message.from_user.id, '''Обрабатываем запрос
это займет около минуты.''', reply_markup=types.ReplyKeyboardRemove())
    prompt = f"Насколько совместимы: {user_list1['znak']} {user_list1['pol']} {user_list1['age']} лет и" \
             f"{user_list2['znak']} {user_list2['pol']} {user_list2['age']} лет"

    # Модель
    completion = openai.Completion.create(engine=engine,
                                          prompt=prompt,
                                          temperature=0.3,
                                          max_tokens=1000)
    bot.send_message(message.from_user.id, completion.choices[0]['text'].split('\n')[-1],
                     reply_markup=types.ReplyKeyboardRemove())

    bot.send_message(message.from_user.id,
                     f"""Напиши мне свой сон а я дам значаение.
Напишите /prediction если хотите узнать предсказание на сегодня
Напишите /compatibility если хотите узнать совместимость двух людей""",
                     reply_markup=types.ReplyKeyboardRemove())


@bot.message_handler(content_types=['text'])
def ans(message):
    bot.send_message(message.from_user.id, f'''Ищу ответ на сон:
{message.text}''', reply_markup=types.ReplyKeyboardRemove())
    bot.send_message(message.from_user.id, '''Обрабатываем запрос
это займет около минуты.''', reply_markup=types.ReplyKeyboardRemove())
    bot.send_message(message.from_user.id, find_ans(message.text), reply_markup=types.ReplyKeyboardRemove())
    bot.send_message(message.from_user.id,
                     f"""Напиши мне свой сон а я дам значаение.
Напишите /prediction если хотите узнать предсказание на сегодня
Напишите /compatibility если хотите узнать совместимость двух людей""",
                     reply_markup=types.ReplyKeyboardRemove())


bot.polling(none_stop=True, interval=0)
