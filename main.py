import argparse
import datetime
import os.path
import time
import urllib.parse
from urllib.parse import urljoin, urlsplit
from pathlib import Path
from pprint import pprint
from urllib.parse import urljoin
import requests
from dotenv import load_dotenv


def fetch_spacex_last_launch(folder, latest_launch_data):

    for image_url in latest_launch_data['links']['flickr']['original']:
        response = requests.get(image_url)
        response.raise_for_status()

        Path(folder).mkdir(exist_ok=True)

        filename = urllib.parse.urlsplit(image_url).path.split('/')[-1]

        with open(Path(folder).joinpath(filename), 'wb') as image_file:
            image_file.write(response.content)

    return


def get_spacex_latest_launches():
    latest_launches_url = 'https://api.spacexdata.com/v5/launches/5ef6a2bf0059c33cee4a828c'

    response = requests.get(latest_launches_url)
    response.raise_for_status()

    if not response.ok:
        return

    latest_launch_data = response.json()
    return latest_launch_data


def get_file_ext(url):

    file_url, filename = os.path.split(urllib.parse.unquote(url))
    file_name, file_ext = os.path.splitext(filename)

    return file_ext


def download_nasa_images(nasa_images_urls, folder):

    Path(folder).mkdir(exist_ok=True)

    for image_url in nasa_images_urls:
        response = requests.get(image_url)
        response.raise_for_status()
        file_url, filename = os.path.split(urllib.parse.unquote(image_url))

        filepath = Path(folder).joinpath(filename)

        with open(filepath, 'wb') as file:
            file.write(response.content)


def download_nasa_epic_images(urls, folder, api_key):
    """ input url - list of urls, folder - folder name, api_key - api_key from NASA API """

    Path(folder).mkdir(exist_ok=True)

    request_data = {
        'api_key': api_key,
    }

    for url in urls:
        response = requests.get(url, params=request_data)
        response.raise_for_status()

        file_url, filename = os.path.split(urllib.parse.unquote(url))

        filepath = Path(folder).joinpath(filename)

        with open(filepath, 'wb') as file:
            file.write(response.content)


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


def get_nasa_epic_urls(api_key):

    url = 'https://api.nasa.gov/EPIC/api/natural/images'

    request_data = {
        'api_key': api_key,
    }

    response = requests.get(url, params=request_data)
    response.raise_for_status()

    epic_images_json = response.json()

    images_url = []

    for epic_image in epic_images_json:

        filename = epic_image['image']

        date_time = datetime.datetime.strptime(filename.split('_')[2], '%Y%m%d%H%M%S')

        images_url.append(f'https://api.nasa.gov/EPIC/archive/natural/{date_time:%Y/%m/%d}/png/{filename}.png')

    return images_url


def main():
    parser = argparse.ArgumentParser(description='Загрузка фото в Telegram')
    args = parser.parse_args()

    load_dotenv()
    token = os.environ['NASA_TOKEN']

    latest_spacex_launch_url = 'https://upload.wikimedia.org/wikipedia/commons/3/3f/HST-SM4.jpeg'

    while True:
        try:

            latest_launch_data = get_spacex_latest_launches()
            fetch_spacex_last_launch('spacex_launches', latest_launch_data)

            nasa_apod_images = get_nasa_apod(token)
            download_nasa_images(nasa_apod_images, 'nasa_apod')

            nasa_epic_urls = get_nasa_epic_urls(token)
            download_nasa_epic_images(nasa_epic_urls, 'nasa_epic', token)

            return

        except requests.exceptions.ConnectionError:
            print(f'Нет связи')
            time.sleep(2)

        except requests.exceptions.HTTPError as error:
            print(f'Ошибка запроса {error}')
            break

        except requests.exceptions.URLRequired:
            print('Ошибка в url')
            return


if __name__ == '__main__':
    main()
