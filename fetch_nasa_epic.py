import datetime
import os
import time
import urllib
from pathlib import Path
import requests
from dotenv import load_dotenv

from functions import download_images


def get_nasa_epic_urls(api_key):

    url = 'https://api.nasa.gov/EPIC/api/natural/images'

    request_data = {
        'api_key': api_key,
    }

    response = requests.get(url, params=request_data)
    response.raise_for_status()

    epic_images = response.json()

    images_url = []

    for epic_image in epic_images:

        filename = epic_image['image']

        date_time = datetime.datetime.strptime(
            filename.split('_')[2],
            '%Y%m%d%H%M%S'
        )

        images_url.append(
            f'https://api.nasa.gov/EPIC/archive/natural/'
            f'{date_time:%Y/%m/%d}/png/{filename}.png'
        )

    return images_url


def main():

    load_dotenv()
    token = os.environ['NASA_TOKEN']

    while True:
        try:

            Path('images').mkdir(exist_ok=True)
            nasa_epic_urls = get_nasa_epic_urls(token)
            download_images(
                nasa_epic_urls,
                'images/nasa_epic',
                {'api_key': token}
            )

            return

        except requests.exceptions.ConnectionError:
            print('Нет связи')
            time.sleep(2)

        except requests.exceptions.HTTPError as error:
            print(f'Ошибка запроса {error}')
            break

        except requests.exceptions.URLRequired:
            print('Ошибка в url')
            return


if __name__ == '__main__':
    main()
