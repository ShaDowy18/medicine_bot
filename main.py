from telebot import types
import string
import config
import telebot
import sqlite3
import schedule
import time
import datetime

bot = telebot.TeleBot(config.token)
res = []
current_shown_dates = []


@bot.message_handler(commands=['time', 'help'])
def set_time(message):
    bot.send_message(message.chat.id, 'Введите время приема лекарств в формате hh:mm')

def set_reminder(message):
    text = message.text
    Htime = text[:2]
    Mtime = text[-2:]
    print(Htime)
    print(Mtime)
    @bot.message_handler(content_types=["text"])
    def reminder(message):
        bot.send_message(message.chat.id, 'Время приема лекарств')


# schedule.every().day.at(time).do(reminder)


@bot.message_handler(content_types=["text"])
def medicine_prep(message):
    conn = sqlite3.connect("drugs.db")
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM Drugs1")
    res = cursor.fetchall()
    name_med_prep = message.text
    t = (name_med_prep,)
    j = 0
    translit_name_med_prep = translit1(name_med_prep)
    translit_name_med_prep.lower()
    keyboard = types.InlineKeyboardMarkup()
    url_pharmacy_button = types.InlineKeyboardButton(text="Поиск в аптеках",
                                                     url="https://infolek.ru/?q=%s" % name_med_prep)
    keyboard.add(url_pharmacy_button)
    url_info_button = types.InlineKeyboardButton(text="Информация о лекарстве",
                                                 url="http://drugdir.ru/preparats/%s" % translit_name_med_prep)
    keyboard.add(url_info_button)
    for i in res:
        if name_med_prep == i[0]:
            cursor.execute("SELECT * FROM Drugs1 WHERE name = '%s'" % t)
            out = cursor.fetchall()
            while j < len(out):
                lst = (out[j])
                j += 1
                message.outp = lst[1] + '\n' + "Краткая информация: " + lst[2] + '\n' + "Рекомендуемая цена: " + str(
                    lst[4])
                bot.send_message(message.chat.id, message.outp, reply_markup=keyboard)
        # else:
        #     message.outp = "Проверьте правильность написания наименования."
        #     Exept(message.chat.id, message.outp)


def translit1(string):
    capital_letters = {
        u'А': u'A',
        u'Б': u'B',
        u'В': u'V',
        u'Г': u'G',
        u'Д': u'D',
        u'Е': u'E',
        u'Ё': u'E',
        u'Ж': u'Zh',
        u'З': u'Z',
        u'И': u'I',
        u'Й': u'Y',
        u'К': u'K',
        u'Л': u'L',
        u'М': u'M',
        u'Н': u'N',
        u'О': u'O',
        u'П': u'P',
        u'Р': u'R',
        u'С': u'S',
        u'Т': u'T',
        u'У': u'U',
        u'Ф': u'F',
        u'Х': u'H',
        u'Ц': u'Ts',
        u'Ч': u'Ch',
        u'Ш': u'Sh',
        u'Щ': u'Sch',
        u'Ъ': u'',
        u'Ы': u'Y',
        u'Ь': u'',
        u'Э': u'E',
        u'Ю': u'Yu',
        u'Я': u'Ya'
    }

    lower_case_letters = {
        u'а': u'a',
        u'б': u'b',
        u'в': u'v',
        u'г': u'g',
        u'д': u'd',
        u'е': u'e',
        u'ё': u'e',
        u'ж': u'zh',
        u'з': u'z',
        u'и': u'i',
        u'й': u'y',
        u'к': u'k',
        u'л': u'l',
        u'м': u'm',
        u'н': u'n',
        u'о': u'o',
        u'п': u'p',
        u'р': u'r',
        u'с': u's',
        u'т': u't',
        u'у': u'u',
        u'ф': u'f',
        u'х': u'h',
        u'ц': u'c',
        u'ч': u'ch',
        u'ш': u'sh',
        u'щ': u'sch',
        u'ъ': u'',
        u'ы': u'y',
        u'ь': u'',
        u'э': u'e',
        u'ю': u'yu',
        u'я': u'ya'
    }

    translit_string = ""

    for index, char in enumerate(string):
        if char in lower_case_letters.keys():
            char = lower_case_letters[char]
        elif char in capital_letters.keys():
            char = capital_letters[char]
            if len(string) > index + 1:
                if string[index + 1] not in lower_case_letters.keys():
                    char = char.upper()
            else:
                char = char.upper()
        translit_string += char

    return translit_string


if __name__ == '__main__':
    bot.polling(none_stop=True)
# import requests
# import datetime
# token = "552495503:AAHJmQJlUqHA3Giml2l-hTLY8szLk2FSxK0"
#
#
# class BotHandler:
#
#     def __init__(self, token):
#         self.token = token
#         self.api_url = "https://api.telegram.org/bot{}/".format(token)
#
#     def get_updates(self, offset=None, timeout=30):
#         method = 'getUpdates'
#         params = {'timeout': timeout, 'offset': offset}
#         resp = requests.get(self.api_url + method, params)
#         result_json = resp.json()['result']
#         return result_json
#
#     def send_message(self, chat_id, text):
#         params = {'chat_id': chat_id, 'text': text}
#         method = 'sendMessage'
#         resp = requests.post(self.api_url + method, params)
#         return resp
#
#     def get_last_update(self):
#         get_result = self.get_updates()
#
#         if len(get_result) > 0:
#             last_update = get_result[-1]
#         else:
#             last_update = get_result[len(get_result)]
#
#         return last_update