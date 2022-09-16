import os
import time
import urllib
from pathlib import Path

import requests
from dotenv import load_dotenv

from functions import download_images


def get_file_ext(url):

    file_url, filename = os.path.split(urllib.parse.unquote(url))
    file_name, file_ext = os.path.splitext(filename)

    return file_ext


def get_nasa_apod(api_key):

    url = 'https://api.nasa.gov/planetary/apod'

    request_params = {
        'api_key':  api_key,
        'count': 10,
    }

    response = requests.get(url, params=request_params)
    response.raise_for_status()

    images = response.json()

    nasa_apod_images = []

    for image in images:
        if get_file_ext(image['url']):
            nasa_apod_images.append(image['url'])

    return nasa_apod_images


def main():

    load_dotenv()
    token = os.environ['NASA_TOKEN']

    while True:
        try:
            Path('images').mkdir(exist_ok=True)
            nasa_apod_images = get_nasa_apod(token)
            download_images(nasa_apod_images, 'images/nasa_apod')

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
