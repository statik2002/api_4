import argparse
import time
import urllib
from urllib.parse import urljoin
from pathlib import Path
import requests

from functions import download_images


def fetch_spacex_last_launch(launch_id='latest'):

    latest_launches_url = urljoin(
        'https://api.spacexdata.com/v5/launches/',
        launch_id
    )

    response = requests.get(latest_launches_url)
    response.raise_for_status()

    latest_launches = response.json()

    latest_launch_images = []
    for image_url in latest_launches['links']['flickr']['original']:
        latest_launch_images.append(image_url)

    return latest_launch_images


def main():
    parser = argparse.ArgumentParser(
        description='скрипт загрузки фотографий запуска компании SpaceX'
    )
    parser.add_argument('--id', help='ID Запуска', default='latest')
    args = parser.parse_args()

    launch_id = args.id

    while True:
        try:
            Path('images').mkdir(exist_ok=True)
            download_images(
                fetch_spacex_last_launch(launch_id),
                'images/spacex_launches',
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
