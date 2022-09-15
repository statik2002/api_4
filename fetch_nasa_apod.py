import os
import time
import urllib
from pathlib import Path

import requests
from dotenv import load_dotenv


def get_file_ext(url):

    file_url, filename = os.path.split(urllib.parse.unquote(url))
    file_name, file_ext = os.path.splitext(filename)

    return file_ext


def get_nasa_apod(api_key):

    url = 'https://api.nasa.gov/planetary/apod'

    request_data = {
        'api_key':  api_key,
        'count': 10,
    }

    response = requests.get(url, params=request_data)
    response.raise_for_status()

    images_info = response.json()

    nasa_apod_images = []

    for image in images_info:
        if get_file_ext(image['url']):
            nasa_apod_images.append(image['url'])

    return nasa_apod_images


def download_nasa_images(nasa_images_urls, folder):

    Path(folder).mkdir(exist_ok=True)

    for image_url in nasa_images_urls:
        response = requests.get(image_url)
        response.raise_for_status()
        file_url, filename = os.path.split(urllib.parse.unquote(image_url))

        filepath = Path(folder).joinpath(filename)

        with open(filepath, 'wb') as file:
            file.write(response.content)


def main():

    load_dotenv()
    token = os.environ['NASA_TOKEN']

    while True:
        try:

            nasa_apod_images = get_nasa_apod(token)
            download_nasa_images(nasa_apod_images, 'nasa_apod')

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
