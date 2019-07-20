import logging
import os

from dotenv import load_dotenv
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

from dialogflow_utils import get_answer
from logs_bot import BotLogsHandler

logger = logging.getLogger('Support Telegram Bot')


def handle_start(bot, update):
    """ Handle start command """

    logger.debug('Received /start command')
    answer = 'Здравствуйте'
    update.message.reply_text(answer)
    logger.debug('Send reply message: {answer}'.format(answer=answer))


def handle_message(bot, update):
    """ Handle all incoming text messages from client with the DialogFlow agent """

    logger.debug('Received text message: {message}'.format(message=update.message.text))
    answer, _ = get_answer(update.message.text, update.message.chat_id)
    update.message.reply_text(answer)
    logger.debug('Send reply message: {answer}'.format(answer=answer))


def main():
    try:
        bot_token = os.environ.get('TG_TOKEN')

        updater = Updater(bot_token)
        dispatcher = updater.dispatcher

        start_handler = CommandHandler('start', handle_start)
        echo_handler = MessageHandler(Filters.text, handle_message)

        dispatcher.add_handler(start_handler)
        dispatcher.add_handler(echo_handler)

        logger.info('Start polling')
        updater.start_polling()
        logger.info('End polling')

    except Exception as ex:
        logger.error(ex, exc_info=True)


if __name__ == '__main__':
    load_dotenv()

    logger.setLevel(logging.INFO)

    logs_bot_token = os.environ.get('LOGS_BOT_TOKEN')
    author_chat_id = os.environ.get('AUTHOR_CHAT_ID')

    if logs_bot_token and author_chat_id:
        logger.addHandler(BotLogsHandler(logs_bot_token, author_chat_id))

    else:
        logger.addHandler(logging.StreamHandler())

    main()
