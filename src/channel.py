import json
import os

# необходимо установить через: pip install google-api-python-client
from googleapiclient.discovery import build

import isodate
def printj(dict_to_print: dict) -> None:
    """Выводит словарь в json-подобном удобном формате с отступами"""
    print(json.dumps(dict_to_print, indent=2, ensure_ascii=False))

class Channel:
    """Класс для ютуб-канала"""
    @classmethod
    def get_service(cls):
        api_key: str = 'AIzaSyCETEaeHEexDGGaWpgJaGe2-9n1FzBqe78'
        youtube = build('youtube', 'v3', developerKey=api_key)
        return youtube
    # YT_API_KEY скопирован из гугла и вставлен в переменные окружения
    # Компьютер корпоративный. Из-за особенностей политик безопасности я не могу установить ключ в переменную среды своего пользователя
    # Поэтому ключ вставляю в код просто строкой
    #api_key: str = 'AIzaSyCETEaeHEexDGGaWpgJaGe2-9n1FzBqe78'

    # создать специальный объект для работы с API
    #youtube = build('youtube', 'v3', developerKey=api_key)

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.channel_id = channel_id
        channel = self.get_service().channels().list(id=self.channel_id, part='snippet,statistics').execute()
        self.id_channel = channel['items'][0]['id']
        self.title = channel['items'][0]['snippet']['title']
        self.description = channel['items'][0]['snippet']['localized']['description']
        self.video_count = channel['items'][0]['statistics']['videoCount']
        self.url = f"https://www.youtube.com/{channel['items'][0]['snippet']['customUrl']}"
        self.subscribers_count = channel['items'][0]['statistics']['subscriberCount']
        self.view_count = channel['items'][0]['statistics']['viewCount']


    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        channel = self.get_service().channels().list(id=self.channel_id, part='snippet,statistics').execute()
        printj(channel)

    def to_json(self, file_name):
        _path = '../homework-2/' + file_name
        with open(_path, 'w', encoding='UTF-8') as file:
            file.write(f'id канала: {self.id_channel}\n'
                       f'Название: {self.title}\n'
                       f'Описание: {self.description}\n'
                       f'Количество видео: {self.video_count}\n'
                       f'URL: {self.url}\n'
                       f'Количество подписчиков: {self.subscribers_count}\n'
                       f'Общее количество просмотров: {self.view_count}')

