import telebot                                                   # Telegram bot module
from re import match,  compile                     # ANALYS WORD
from db import read_db, write_db                # database functions
database = read_db()
bot = telebot.TeleBot(database['token'])


def is_bad(word, bad, excepts):  # check bad words
    # Replace spec.symbols
    # Excepts
    if word in excepts:
        return False
    # Agressive mode, causes false positives
    # res = search(bad, word)
    res = match(bad, word)
    if res is not None:
        return True
    else:
        return False


def rep(word):  # TRANSLIT an OTHER
    symbols = [['e', 'е'], ['a', 'а'], ['i', 'и'], ['t', 'т'], ['y', 'у'], ['u', 'у'], ['o', 'о'], ['d', 'д'], ['x', 'х'],
                        ['t', 'т'], ['p', 'п'], ['r', 'р'], ['h', 'х'], ['b', 'б'], ['n', 'н'],
                        ['🇽', 'х'], ['🇾', 'у'], ['🇹', 'т'], ['🇪', 'е'], ['❌', 'х'], ['✖', 'х'], ['❎', 'х']]
    for symbol in symbols:
        word = word.replace(symbol[0], symbol[1])
    return word


def catch(message):  # CATCH BAD WORDS
    bad_list = ['ху.+й', 'х.+уй', 'xуи', 'xyи', 'хyи', 'xyй', 'xуй', 'ху.', '.+хуе', '.+хуё', 'xyu', 'xui', 'хyй',
                'поху', '.уй', 'ах.ен', 'а.уе', '.+хуй', '.+хуй', 'хуя', '.+хуя',
                'бл.+ть', 'бля', 'бл.+ть', '.+бл+.дь+', '.+бл.+дь',
                'трах', 'еб.+ть', 'ебу', 'ебал', '..ебен', 'ёбан', 'ебть', 'eby', '..ебись', 'уеб', 'уёб', 'ебей', 'ебу', 'ебл', 'еба',
                '.+ебн.+т.+', '.+еб.ть', 'ебо', '.+ебо', '.+еба', '.+ёбы', 'еби.+', 'ёба.+', 'ебля', 'ебё.+', 'заеб', 'заеб.+', 'заёб',
                '.+заеб', '.+заёб', 'заеб.+', 'заёб.+', 'ёбск', '.+ебуч.+',
                'еб.+утые', 'е.+б.+утые', 'ебан', 'еб.+н', 'ебн', 'ёбн', '.+ёбка', '.+ебка',
                'пр..ба', '.б.л', 'у.б', '.блан',
                '.+пизд', 'пизец', 'пздец', 'п.+здец', 'пизд', '.+пизж.+',
                'пид.+р', 'пидр',
                'д.лб.+б',
                'f.+ck', 's.+ck', 'fck', 'sck']

    excepts = ['хороший', 'хороший.', 'убил', 'убил.']
    words = message.text.split()
    bad_found = False
    for check in words:
        # Mat -> Мат
        check = rep(check)
        # -М#ат$ => Мат
        regex = compile('[^a-zA-Zа-яА-ЯЁё]')
        check = regex.sub('', check)
        if bad_found:
            break
        for bad in bad_list:
            if is_bad(check.lower(), bad, excepts):
                bad_found = True
                break
    if not bad_found:
        for check in words:
            check = rep(check)
            regex = compile('[^a-zA-Zа-яА-ЯЁё]')
            check = regex.sub('.', check)
            if bad_found:
                break
            for bad in bad_list:
                if is_bad(check.lower(), bad, excepts):
                    bad_found = True
                    break
    if bad_found:
        database = read_db()
        chat_id = str(message.chat.id)
        user_id = str(message.from_user.id)
        if chat_id not in database:
            database[chat_id] = {}
        if user_id not in database[chat_id]:
            database[chat_id][user_id] = {}
            database[chat_id][user_id]["lunch"] = 0
        if user_id in database[chat_id]:
            database[chat_id][user_id]["lunch"] += 1
        bot.send_message(message.chat.id,
                             f'<a href="tg://user?id={user_id}">Пользователь</a> использовал непечатное выражение.\n'
                             f'Кол-во потерянных обедов: {database[chat_id][user_id]["lunch"]}',
                             parse_mode='HTML')
        write_db(database)


@bot.message_handler(commands=['stats'])  # stats
def send_stats(message):
    database = read_db()
    chat_id = str(message.chat.id)
    user_id = str(message.from_user.id)
    if user_id not in database[chat_id]:
        database[chat_id] = {}
        database[chat_id][user_id] = {}
        database[chat_id][user_id]["lunch"] = 0
    else:
        lunch_count = database[chat_id][user_id]["lunch"]
        if lunch_count > 0:
            if lunch_count == 1: obed = "обеда"
            else: obed = "обедов"
            bot.send_message(chat_id, f'<a href="tg://user?id={user_id}">Вы</a> убили {database[chat_id][user_id]["lunch"]} {obed}! Ужас...', parse_mode='HTML')
        else:
            bot.send_message(chat_id, f'<a href="tg://user?id={user_id}">Вы</a> не убили ни одного обеда сегодня, поздравляю!', parse_mode='HTML')


@bot.message_handler()
def catch_all_messages(message):
    catch(message)


@bot.edited_message_handler()
def catch_edited_messages(message):
    catch(message)


def main():
    mod = 1
    if mod == 1:
        while True:
            try:
                bot.polling()
            except KeyboardInterrupt:
                exit()
            except:
                pass
    elif mod == 2:
        bot.polling()
    else:
        exit()


if __name__ == "__main__":
    main()
