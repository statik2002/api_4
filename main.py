import argparse
import datetime
import os
import random
import time
from pathlib import Path
from pprint import pprint

from dotenv import load_dotenv
import telegram

import fetch_nasa_apod
import fetch_nasa_epic
import fetch_spacex_images
from PIL import Image


def resize_image(image):
    work_image = Image.open(image)
    image_w, image_h = work_image.size

    #print(work_image.size)

    if image_h > 1000 or image_w > 1000:
        fixed_width = 1000
        width_percent = fixed_width / float(image_w)
        height_percent = int((float(image_h) * float(width_percent)))
        print(width_percent, height_percent)
        new_image = work_image.resize((fixed_width, height_percent))
        return new_image

    return work_image


def send_photo_in_telegram(bot, chat_id):

    for root, dirs, files in os.walk('images'):
        random.shuffle(files)
        for file in files:
            img = resize_image(os.path.join(root, file))
            return_message = bot.sendPhoto(
                chat_id=chat_id,
                photo=open(img, 'rb')
            )
            if not return_message:
                raise telegram.error


def main():

    parser = argparse.ArgumentParser(
        description='скрипт загрузки фотографий и выгрузки в telegram'
    )
    parser.add_argument('-p', '--period', help='Период для обновления', default='4')
    args = parser.parse_args()

    period = args.period

    load_dotenv()
    telegram_token = os.environ['TELEGRAM_TOKEN']
    chat_id = os.environ['CHAT_ID']

    bot = telegram.Bot(token=telegram_token)

    last_time_posted = datetime.datetime.now()

    #fetch_nasa_apod.main()
    #fetch_nasa_epic.main()
    #fetch_spacex_images.main()
    send_photo_in_telegram(bot, chat_id=chat_id)

    while True:

        if datetime.datetime.now()-last_time_posted > datetime.timedelta(hours=int(period)):

            #fetch_nasa_apod.main()
            #fetch_nasa_epic.main()
            #fetch_spacex_images()

            try:
                send_photo_in_telegram(bot, chat_id=chat_id)

            except telegram.error as error:
                print(f'Error - {error}')

            last_time_posted = datetime.datetime.now()

        time.sleep(5)


if __name__ == '__main__':
    main()
