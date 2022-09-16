import argparse
import datetime
import os
import random
import time

from dotenv import load_dotenv
import telegram

import fetch_nasa_apod
import fetch_nasa_epic
import fetch_spacex_images


def send_photo_in_telegram(bot, chat_id):

    for root, dirs, files in os.walk('images'):
        random.shuffle(files)
        for file in files:
            return_message = bot.sendPhoto(
                chat_id=chat_id,
                photo=open(os.path.join(root, file), 'rb')
            )
            if not return_message:
                raise telegram.error


def main():

    load_dotenv()
    telegram_token = os.environ['TELEGRAM_TOKEN']
    chat_id = '@chatbotdevmantest'
    period = os.environ['PERIOD']

    bot = telegram.Bot(token=telegram_token)

    last_time_posted = datetime.datetime.now()

    fetch_nasa_apod.main()
    fetch_nasa_epic.main()
    fetch_spacex_images.main()
    send_photo_in_telegram(bot, chat_id=chat_id)

    while True:

        if datetime.datetime.now()-last_time_posted > \
                datetime.timedelta(hours=int(period)):

            fetch_nasa_apod.main()
            fetch_nasa_epic.main()
            fetch_spacex_images()

            try:

                send_photo_in_telegram(bot, chat_id=chat_id)
                time.sleep(3)

            except telegram.error as error:
                print(f'Error - {error}')

            last_time_posted = datetime.datetime.now()

        time.sleep(5)


if __name__ == '__main__':
    main()
