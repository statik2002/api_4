import argparse
import time
import urllib
from urllib.parse import urljoin
from pathlib import Path
import requests


def get_spacex_latest_launches(launch_id):
    latest_launches_url = urljoin(
        'https://api.spacexdata.com/v5/launches/',
        launch_id
    )

    response = requests.get(latest_launches_url)
    response.raise_for_status()

    latest_launch_data = response.json()
    return latest_launch_data


def fetch_spacex_last_launch(folder, latest_launch_data):

    for image_url in latest_launch_data['links']['flickr']['original']:
        response = requests.get(image_url)
        response.raise_for_status()

        Path(folder).mkdir(exist_ok=True)

        filename = urllib.parse.urlsplit(image_url).path.split('/')[-1]

        with open(Path(folder).joinpath(filename), 'wb') as image_file:
            image_file.write(response.content)

    return


def main():
    parser = argparse.ArgumentParser(
        description='скрипт загрузки фотографий запуска компании SpaceX'
    )
    parser.add_argument('-id', help='ID Запуска', default='latest')
    args = parser.parse_args()

    launch_id = args.id

    while True:
        try:

            latest_launch_data = get_spacex_latest_launches(launch_id)
            fetch_spacex_last_launch('spacex_launches', latest_launch_data)

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
