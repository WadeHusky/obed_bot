import schedule
from time import sleep
import telebot
from db import read_db, write_db
token = read_db()["token"]
bot = telebot.TeleBot(token)


def send_message():
    database = read_db()
    for chat_id in database:
        text = 'Статистика обедов за 24 часа:\n'
        if chat_id != "token":
            for user_id in database[chat_id]:
                lunch = database[chat_id][user_id]["lunch"]
                if lunch > 0:
                    if lunch == 1: obed = "обеда"
                    else: obed = "обедов"
                    text += f'<a href="tg://user?id={user_id}">Пользователь</a> убил {lunch} {obed}😿\n'
                    database[chat_id][user_id]["lunch"] = 0
                else:
                    text += f'<a href="tg://user?id={user_id}">Пользователь</a> молодец!\n'
            write_db(database)
            bot.send_message(int(chat_id), text, parse_mode='HTML')


def main():
    schedule.every().day.at('21:00', 'Europe/Moscow').do(send_message)
    while True:
        try:
            schedule.run_pending()
            sleep(1)
        except:
            pass


if __name__ == "__main__":
    main()
