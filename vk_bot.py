import os
import random

from dotenv import load_dotenv
from vk_api import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType

from dialogflow_utils import get_answer


def handle_message(event, session_api):
    """ Handle all incoming messages from client with the DialogFlow agent """

    answer, intent = get_answer(event.text, event.user_id)

    if intent != 'Default Fallback Intent':
        session_api.messages.send(
            user_id=event.user_id,
            message=answer,
            random_id=random.randint(1, 1000)
        )


def main():
    """ Long polling Bot for VK group """

    load_dotenv()

    vk_token = os.environ.get('VK_TOKEN')

    vk_session = vk_api.VkApi(token=vk_token)
    session_api = vk_session.get_api()
    polling = VkLongPoll(vk_session)

    for event in polling.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            handle_message(event, session_api)


if __name__ == '__main__':
    main()
