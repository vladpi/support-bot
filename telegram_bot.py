import os

from dotenv import load_dotenv
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

from dialogflow_utils import get_answer


def handle_start(bot, update):
    """ Handle start command """

    update.message.reply_text('Здравствуйте')


def handle_message(bot, update):
    """ Handle all incoming text messages from client with the DialogFlow agent """

    answer, _ = get_answer(update.message.text, update.message.chat_id)
    update.message.reply_text(answer)


def main():
    load_dotenv()

    bot_token = os.environ.get('TG_TOKEN')

    updater = Updater(bot_token)
    dispatcher = updater.dispatcher

    start_handler = CommandHandler('start', handle_start)
    echo_handler = MessageHandler(Filters.text, handle_message)

    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(echo_handler)

    updater.start_polling()


if __name__ == '__main__':
    main()
