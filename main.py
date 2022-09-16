import argparse
import datetime
import os
import random
import time
from pathlib import Path

from dotenv import load_dotenv
import telegram

import fetch_nasa_apod
import fetch_nasa_epic
import fetch_spacex_images
from functions import download_images


def send_photo_in_telegram(bot, chat_id):

    for root, dirs, files in os.walk('images'):
        random.shuffle(files)
        for file in files:
            with open(os.path.join(root, file), 'rb') as image_file:
                return_message = bot.sendPhoto(
                    chat_id=chat_id,
                    photo=image_file
                )
                if not return_message:
                    raise telegram.error


def main():

    load_dotenv()
    telegram_token = os.environ['TELEGRAM_TOKEN']
    chat_id = os.environ['CHAT_ID']
    period = os.environ['PERIOD']
    nasa_token = os.environ['NASA_TOKEN']

    bot = telegram.Bot(token=telegram_token)

    last_time_posted = datetime.datetime.now() - datetime.timedelta(hours=int(period))

    main_path = 'images'

    Path(main_path).mkdir(exist_ok=True)

    while True:

        if datetime.datetime.now()-last_time_posted > \
                datetime.timedelta(hours=int(period)):

            download_images(
                fetch_nasa_apod.get_nasa_apod(nasa_token),
                Path(main_path).joinpath('nasa_apod')
            )
            download_images(
                fetch_nasa_epic.get_nasa_epic_urls(nasa_token),
                Path(main_path).joinpath('nasa_epic'),
                {'api_key': nasa_token}
            )
            download_images(
                fetch_spacex_images.fetch_spacex_last_launch(),
                Path(main_path).joinpath('spacex_latest')
            )

            try:

                send_photo_in_telegram(bot, chat_id=chat_id)
                time.sleep(3)

            except telegram.error as error:
                print(f'Error - {error}')

            last_time_posted = datetime.datetime.now()

        time.sleep(5)


if __name__ == '__main__':
    main()
