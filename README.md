# Урок 4 по API

4 cкрипта:
- `fetch_nasa_apod.py` загрузка APOD изображений с сайта NASA
- `fetch_spacex_images.py` загрузка последних запусков компании SpaceX
- `fetch_nasa_epic.py` загрузка EPIC изображение с сайта NASA
- `main.py` - отправка загруженных изображений в telegram канал с определенной периодичностью.

В результате работы скриптов, будут созданы 3 папки с изображениями spacex_launches, nasa_apod и nasa_epic

## Установка

- Получить API_KEY на сайте NASA `https://api.nasa.gov/`
- Получить API-токен Telegram
- Создать файл `.env` и создать переменную окружения `NASA_TOKEN=<API_KEY>`, `TELEGRAM_TOKEN=<API_TOKEN>`, `PERIOD=4`
- В переменной PERIOD указываем количество часов между отсылкой картинок
- Установить зависимости командой 
  > `pip install requirements.txt`

## Использование 

- Запустить скрипт командой 

  > `python main.py -p [int]`
  
  При запуске без параметров время отправки картинок по умолчанию 4 часа, при запуске с параметром -h указываем
время обновления в часах. Скрипт автоматически скачивает картинки APOD, EPIC и SpaceX_latest_launches.
 без параметров, скачивает фото последнего запуска, либо параметр={id launch}"

  > `python fetch_nasa_apod.py`

  > `python fetch_nasa_epic.py`

  > `python fetch_spacex_images.py`
  
  