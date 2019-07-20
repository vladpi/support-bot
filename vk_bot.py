import logging
import os
import random

from dotenv import load_dotenv
from vk_api import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType

from dialogflow_utils import get_answer
from logs_bot import BotLogsHandler

logger = logging.getLogger('Support VK Bot')


def handle_message(event, session_api):
    """ Handle all incoming messages from client with the DialogFlow agent """

    logger.debug('Received text message: {message}'.format(message=event.text))

    answer, intent = get_answer(event.text, event.user_id)

    if intent != 'Default Fallback Intent':
        session_api.messages.send(
            user_id=event.user_id,
            message=answer,
            random_id=random.randint(1, 1000)
        )
        logger.debug('Send reply message: {answer}'.format(answer=answer))


def main():
    """ Long polling Bot for VK group """

    try:
        vk_token = os.environ.get('VK_TOKEN')

        vk_session = vk_api.VkApi(token=vk_token)
        session_api = vk_session.get_api()
        polling = VkLongPoll(vk_session)

        logger.info('Start polling')

        for event in polling.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                handle_message(event, session_api)

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
