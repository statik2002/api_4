import os
from pprint import pprint

from dotenv import load_dotenv
import telegram


def main():
    load_dotenv()
    telegram_token = os.environ['TELEGRAM_TOKEN']

    bot = telegram.Bot(token=telegram_token)

    bot_params = bot.get_me()

    updates = bot.get_updates()
    chat_id = updates[0]['my_chat_member']['chat']['id']

    bot.sendMessage(text='Look at this image', chat_id=chat_id)
    bot.send_document(chat_id=chat_id, document=open('nasa_apod/beltofvenus_churchill.jpg', 'rb'))


if __name__ == '__main__':
    main()
