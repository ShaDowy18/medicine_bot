import os
import telebot
from flask import Flask, request

import config

bot = telebot.TeleBot(config.token)
bot.stop_polling()

HOST = "0.0.0.0"
PORT = os.environ.get('PORT', 8443)

server = Flask(__name__)
@bot.message_handler(commands=["start"])
def handle_start(message):
    bot.send_message(message.from_user.id,
                     "Добро пожаловать \n")
@server.route('/bot', methods=['POST'])
def getMessage():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return '/bot', 200


@server.route('/')
def webhook_handler():
    bot.remove_webhook()
    bot.set_webhook(url=config.heroku_webhook)
    status_msg = "i'm live. listening on %s:%s" % (HOST, PORT)
    return status_msg, 200


# Remove webhook, it fails sometimes the set if there is a previous webhook
bot.remove_webhook()

# Set webhook
bot.set_webhook(url=config.heroku_webhook)

# bot.polling(none_stop=True)
server.run(host=HOST, port=PORT)
