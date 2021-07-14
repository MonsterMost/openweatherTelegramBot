from telebot import TeleBot
# Библиотека для работы с телеграм API Потом через BotFather надо создать теоеграм бота и получить токен
import functions


# Сохранили токен
token = '1718825708:AAGTz4T55FYXeKe3aDPF4w3nFeXXgEe9rLM'

# Надо подключиться к нашему боту
bot = TeleBot(token, parse_mode='HTML')
owner = '84779542'


# Первое что мы делаем это запускаем бота. Для отлова команды /start есть декораторы

@bot.message_handler(commands=['start'])  # отлов команд телеграма можно написать не только start
def command_start(message):  # При работе с ботом мы получаем сообщения, с которыми и будем работать
    chat_id = message.chat.id  # Лучше сохранить если планируем много раз использовать в функции
    first_name = message.chat.first_name
    # Если функция большая то лучше сохранить в переменную чтобы часто не обращаться
    bot.send_message(chat_id, f'Привет, {first_name}!')
    print(message)  # message как экземпляр класса поэтому обращаемся через . методы
    insert_city_name(message)  # передаем message и запускаем эту функцию сразу после выполнения command_start


@bot.message_handler(content_types=['text'])
def get_text(message):
    if message.text != '/start':
        reply_to_user(message)


def insert_city_name(message):
    chat_id = message.chat.id
    msg = bot.send_message(chat_id=chat_id,
                           text='Введите название города: ')  # именнованное передавание для понимания больших значений
    bot.register_next_step_handler(msg, reply_to_user)  # спец функция которая говорит, что после msg к тому что будет
    # написано юзером примени функцию reply_to_user


# Бот должен ждать ответа после insert_city_name, для того чтобы это сработало обернем в переменную msg строку 25
def reply_to_user(message):  # функция ответа юзеру
    print(message)
    chat_id = message.chat.id  # сохраняем id пользователя
    user_text = message.text  # сохраняем его сообщение
    # Проверка на стоп слово
    if user_text.lower() in ['stop', '/stop']:
        bot.send_message(chat_id, 'Бот остановлен. Для запуска нажмите /start')
        return
    message_to_user = functions.get_weather_by_city_name(user_text)  # Вызов функции и генерация сообщения
    # msg = bot.reply_to(message, message_to_user, parse_mode='HTML')  # Мод отображения чтобы работало <b></b>
    msg = bot.reply_to(message, message_to_user)
    # Реплай на сообщение пользователя (Отвечать на что, чем отвечать)
    # insert_city_name(message)  # Чтобы он опять попросил название города
    # Закоментим insert_city_name(message) чтобы сделать по другому
    bot.register_next_step_handler(msg, reply_to_user)  # Просто ждем ввода слова без просьбы что-то ввести

    message_to_me = f'''Сообщение от @{message.from_user.username}
Имя пользователя: {message.from_user.first_name}
Текст сообщения: {message.text}
Ответ {message_to_user}
'''
    bot.send_message(owner, message_to_me)


# Зацикливаем бота, чтобы он не останавливался none-stop = True
# чтобы некоторые get запросы не ломали бота, а давали замечание
print('Бот работает...')
bot.polling(none_stop=True)


