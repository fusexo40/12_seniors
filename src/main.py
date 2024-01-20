import telebot
import os
import sqlite3
import time
from dotenv_vault import load_dotenv
from structures.UserProfile import UserProfile
from scripts.create_db import CreateDB
from telebot import types


CreateDB()
load_dotenv()
token = os.getenv("token")
bot = telebot.TeleBot(token)
tconv = lambda x: time.strftime("%H:%M:%S %d.%m.%Y", time.localtime(x))
subject_list = ["Английский язык", "Алгебра", "Геометрия", "Физика", "Информатика", "Русский язык", "Литература", "Биология", "Химия", "География", "История", "Обществознание"]
st = []


@bot.message_handler(commands=['start'])
def start(message):
    markup = telebot.types.ReplyKeyboardRemove()
    connection = sqlite3.connect('users.db')
    cursor = connection.cursor()
    info = cursor.execute('SELECT id FROM users WHERE id=?', (message.from_user.id, ))
    if info.fetchone() is None:
        bot.send_message(message.chat.id, "Привет 👋! Похоже вы не зарагестрированны. Введите класс в котором вы учитесь", reply_markup=markup)
    else:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(types.KeyboardButton("Привет 👋!"))
        bot.send_message(message.chat.id, f"Привет 👋, {message.from_user.username}!", reply_markup=markup)
    bot.register_next_step_handler(message, add_user)


def add_user(message):
    username = message.from_user.username
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton("❓ Задать вопрос"), types.KeyboardButton("Профиль 🆔"), types.KeyboardButton("Ссылка на тгк 📎"))
    bot.send_message(message.chat.id, f"Я телеграм бот 🤖 для взаимопомощи ученикам 👨‍🎓. Все вопросы❔ и ответы❕ находятся в нашем телеграм канале", reply_markup=markup)
    if message.text != "В главное меню ⬅️" and message.text != "Привет 👋!":
        id = message.from_user.id
        if int(message.text) >= 0 and int(message.text) <= 11:
            form = message.text
            connection = sqlite3.connect('users.db')
            cursor = connection.cursor()
            info = cursor.execute('SELECT * FROM users WHERE id=?', (id, ))
            if info.fetchone() is None: 
                cursor.execute(f"""
                INSERT INTO users (id, username, form, rating) VALUES ({id}, '{username}', {form}, 1000)
                """)
            else:
                db_username = cursor.execute('SELECT username FROM users WHERE id=?', (id, ))
                if db_username != username:
                    cursor.execute(f"""
                    UPDATE users SET username = '{username}' WHERE id = {id}
                    """
                    )
                cursor.execute(f"""
                UPDATE users SET form = {form} WHERE id = {id}
                """
                )
            connection.commit()
            connection.close()
    

@bot.message_handler(content_types=['text'])
def func(message):
    if message.text == "❓ Задать вопрос":
        markup = telebot.types.ReplyKeyboardRemove()
        st = []
        bot.send_message(message.chat.id, "Напишите вопрос ⌨️❓", reply_markup=markup)
        bot.register_next_step_handler(message, ask_q, st)
    elif message.text == "Профиль 🆔":
        connection = sqlite3.connect('users.db')
        cursor = connection.cursor()
        countquestions = len(cursor.execute('SELECT question FROM questions WHERE author_id=?', (message.from_user.id, )).fetchall())
        rating = 1000
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(types.KeyboardButton("Мои вопросы 📝"), types.KeyboardButton("В главное меню ⬅️"))
        bot.send_message(message.chat.id,
                         text=f"Ник: {message.from_user.username}\nРейтинг: {rating}\nАктивные вопросы: {countquestions}", reply_markup=markup)
        connection.commit()
        connection.close()
    elif message.text == "Ссылка на тгк 📎":
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("Ссылка 📎", url='https://t.me/hahaton24'))
        bot.send_message(message.chat.id, "Наш телеграмм канал", reply_markup=markup)
    elif message.text == "В главное меню ⬅️":
        add_user(message)
    elif message.text == "Мои вопросы 📝":
        connection = sqlite3.connect('users.db')
        cursor = connection.cursor()
        info = cursor.execute('SELECT question FROM questions WHERE author_id=?', (message.from_user.id, )).fetchall()
        info2 = cursor.execute('SELECT question_id FROM questions WHERE author_id=?', (message.from_user.id, )).fetchall()
        if len(info) == 0 or len(info2) == 0:
            bot.send_message(message.chat.id, "У вас нет активных вопросов")
        else:
            result = []
            for i in range(1, len(info) + 1):
                result.append(f'{i}. {info[i - 1][0]} - https://t.me/hahaton24/{info2[i - 1][0] + 136}\n')
            bot.send_message(message.chat.id, "".join(result))
        connection.commit()
        connection.close()


def ask_q(message, st):
    st.append(message.text)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for i in subject_list:
        markup.add(types.KeyboardButton(i))
    bot.send_message(message.chat.id, f"Выберите предмет 📕 к которому относится этот вопрос ➡️", reply_markup=markup)
    bot.register_next_step_handler(message, subject, st)


def subject(message, st):
    st.append(message.text)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for i in range(1, 12):
        markup.add(types.KeyboardButton(str(i)))
    bot.send_message(message.chat.id, f"Выберите класс 👩‍🏫 к которому относится этот вопрос❓", reply_markup=markup)
    bot.register_next_step_handler(message, class_number, st)


def class_number(message, st):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton("В главное меню ⬅️"))
    st.append(message.text)
    connection = sqlite3.connect('users.db')
    cursor = connection.cursor()
    info = cursor.execute("SELECT question FROM questions")
    match = False
    questions_list = info.fetchall()
    for i in questions_list:
        if st[0] == i[0]:
            match = True
    if match:
        q_id = (cursor.execute('SELECT question_id FROM questions WHERE question=?', (st[0], )).fetchone())[0]
        bot.send_message(message.chat.id, f"В нашем телеграм канале обнаружен такой же вопрос. Вы можете его найти по этому номеру {q_id}")
    else:
        cursor.execute(f"INSERT INTO questions (question, create_date, author_id) VALUES ('{st[0]}', '{tconv(message.date)}', {int(message.from_user.id)})")
        bot.send_message(message.chat.id, "Похоже, что вашего вопроса еще не было в нашем телеграм канале")
        q_id = len(cursor.execute('SELECT question FROM questions').fetchall())
        bot.send_message("-1002010810009", f'Вопрос №{q_id}\n{st[0]}\n#{"".join(st[1].split(" "))} \n#{st[2]}_класс')
        bot.send_message(message.chat.id, f"Ваш вопрос отправлен в телеграм канал ✅", reply_markup=markup)
    connection.commit()
    connection.close()
    st = []


bot.polling(none_stop=True, interval=0)