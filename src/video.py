import json
import os

# необходимо установить через: pip install google-api-python-client
from googleapiclient.discovery import build

import isodate
def printj(dict_to_print: dict) -> None:
    """Выводит словарь в json-подобном удобном формате с отступами"""
    print(json.dumps(dict_to_print, indent=2, ensure_ascii=False))

class Video:

    @classmethod
    def get_service(cls):
        """Создаёт специальный объект для работы с API youtube"""
        # Компьютер корпоративный. Из-за особенностей политик безопасности я не могу установить ключ в переменную среды своего пользователя
        # Поэтому ключ вставляю в код просто строкой
        api_key: str = '******'
        youtube = build('youtube', 'v3', developerKey=api_key)
        return youtube

    @property
    def video_id(self):
        return self.__video_id


    def __init__(self, video_id: str):
        self.__video_id = video_id
        self.video = self.get_service().videos().list(part='snippet,statistics,contentDetails,topicDetails', id=self.__video_id).execute()
        try:
            self.video['items'][0]
        except IndexError:
            self.video_title = None
            self.url = None
            self.view_count = None
            self.like_count = None
        else:
            self.video_title = self.video['items'][0]['snippet']['title']
            self.url = f"https://www.youtube.com/watch?v={self.__video_id}"
            self.view_count = self.video['items'][0]['statistics']['viewCount']
            self.like_count = self.video['items'][0]['statistics']['likeCount']

    def print_video_info(self):
        """Выводит в консоль информацию о канале."""
        video = self.get_service().videos().list(part='snippet,statistics,contentDetails,topicDetails', id=self.__video_id).execute()
        printj(video)

    def __str__(self):
        return self.video_title

class PLVideo(Video):
    def __init__(self, video_id: str, playlist_id: str):
        super().__init__(video_id)
        self.__playlist_id = playlist_id

    @property
    def playlist_id(self):
        return self.__playlist_id
