import os
import urllib
from pathlib import Path
import requests


def download_images(urls, folder, params={}):

    Path(folder).mkdir(exist_ok=True)

    for url in urls:
        response = requests.get(url, params=params)
        response.raise_for_status()

        file_url, filename = os.path.split(urllib.parse.unquote(url))

        filepath = Path(folder).joinpath(filename)

        with open(filepath, 'wb') as file:
            file.write(response.content)
