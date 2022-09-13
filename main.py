import argparse
import os.path
import time
import urllib.parse
from pathlib import Path
from pprint import pprint
from urllib.parse import urljoin
import requests


def fetch_spacex_last_launch(path, latest_launch_data):

    for image_url in latest_launch_data['links']['flickr']['original']:
        response = requests.get(image_url)
        response.raise_for_status()

        if not Path(path).exists():
            Path(path).mkdir()

        filename = urllib.parse.urlsplit(image_url).path.split('/')[-1]

        with open(Path(path).joinpath(filename), 'wb') as image_file:
            image_file.write(response.content)

    return


def get_spacex_latest_launches():
    latest_launches_url = 'https://api.spacexdata.com/v5/launches/5ef6a2bf0059c33cee4a828c'

    response = requests.get(latest_launches_url)
    response.raise_for_status()

    if not response.ok:
        return

    latest_launch_data = response.json()
    fetch_spacex_last_launch('images', latest_launch_data)


def main():
    parser = argparse.ArgumentParser(description='Загрузка фото в Telegram')
    args = parser.parse_args()

    url = 'https://upload.wikimedia.org/wikipedia/commons/3/3f/HST-SM4.jpeg'

    while True:
        try:
            #load_image('images/', url)
            get_spacex_latest_launches()
            return

        except requests.exceptions.ConnectionError:
            print(f'Нет связи')
            time.sleep(2)

        except requests.exceptions.HTTPError:
            print(f'Ошибка запроса')
            break

        except requests.exceptions.URLRequired:
            print('Ошибка в url')
            return


if __name__ == '__main__':
    main()
