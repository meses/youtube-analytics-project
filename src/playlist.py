import json
import os
import datetime
import isodate

# необходимо установить через: pip install google-api-python-client
from googleapiclient.discovery import build
def printj(dict_to_print: dict) -> None:
    """Выводит словарь в json-подобном удобном формате с отступами"""
    print(json.dumps(dict_to_print, indent=2, ensure_ascii=False))
class PlayList:
    @classmethod
    def get_service(cls):
        """Создаёт специальный объект для работы с API youtube"""
        # Компьютер корпоративный. Из-за особенностей политик безопасности я не могу установить ключ в переменную среды своего пользователя
        # Поэтому ключ вставляю в код просто строкой
        api_key: str = '*****'
        youtube = build('youtube', 'v3', developerKey=api_key)
        return youtube


    def __init__(self, playlist_id: str):
        self.__playlist_id = playlist_id
        self.__playlist_videos = self.get_service().playlistItems().list(playlistId=self.__playlist_id,
                                               part='contentDetails',
                                               maxResults=50,
                                               ).execute()
        self.__playlists_info = self.get_service().playlists().list(id=playlist_id, part='contentDetails,snippet', maxResults=50, ).execute()
        self.__title = self.__playlists_info['items'][0]['snippet']['title']
        self.__url = f"https://www.youtube.com/playlist?list={self.__playlist_id}"
        self.__video_ids: list[str] = [video['contentDetails']['videoId'] for video in self.__playlist_videos['items']]
        self.__video_response = self.get_service().videos().list(part='contentDetails, statistics', id=','.join(self.__video_ids)).execute()

    def print_playlist_info(self):
        """Выводит в консоль информацию о плейлисте."""
        playlist = self.__playlists_info
        printj(playlist)

    def print_playlist_video_info(self):
        """Выводит в консоль информацию об id и дате публикации всех видео в плейлисте."""
        playlist = self.__playlist_videos
        printj(playlist)

    @property
    def title(self):
        return self.__title

    @property
    def url(self):
        return self.__url

    def video_response(self):
        """Выводит в консоль информацию и статистику о видео в плейлисте"""
        videos = self.__video_response
        printj(videos)

    @property
    def total_duration(self):
        """Выводит в консоль общую длительность всех видео в плейлисте"""
        total_duration = datetime.timedelta()
        video_response = self.__video_response

        for video in video_response['items']:
            iso_8601_duration = video['contentDetails']['duration']
            duration = isodate.parse_duration(iso_8601_duration)
            total_duration += duration
        return total_duration

    def show_best_video(self):
        """Выводит сслыку на видео с наибольшим количеством лайков"""
        video_list = self.__video_response
        max_likes = 0
        max_likes_video = None

        for i in range(int(video_list['pageInfo']['totalResults'])):
            like_count = int(video_list['items'][i]['statistics']['likeCount'])
            if like_count > max_likes:
                max_likes = like_count
                max_likes_video = video_list['items'][i]['id']
        return f"https://youtu.be/{max_likes_video}"

