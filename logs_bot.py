import logging

from telegram import Bot


class BotLogsHandler(logging.Handler):
    def __init__(self, bot_token, author_chat_id):
        super(BotLogsHandler, self).__init__()
        self.bot = Bot(token=bot_token)
        self.chat_id = author_chat_id

    def emit(self, record):
        log_entry = self.format(record)
        message_text = '{logger_name}:\n{text}'.format(logger_name=record.name, text=log_entry)
        self.bot.send_message(chat_id=self.chat_id, text=message_text)
