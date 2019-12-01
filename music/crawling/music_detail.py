import requests
import random
import json

from datetime import datetime
from typing import List, AnyStr, Optional


class MusicDetail:
    USER_AGENT_LIST = [
        'Mozilla/5.0 (Linux; Android 4.4.2; XMP-6250 Build/HAWK) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/30.0.0.0 Safari/537.36 ADAPI/2.0 (UUID:9e7df0ed-2a5c-4a19-bec7-2cc54800f99d) RK3188-ADAPI/1.2.84.533 (MODEL:XMP-6250)',
        'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/11.1.2 Safari/605.1.15',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/602.4.8 (KHTML, like Gecko) Version/10.0.3 Safari/602.4.8',
        'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36 OPR/48.0.2685.52',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/603.3.8 (KHTML, like Gecko) Version/10.1.2 Safari/603.3.8',
    ]

    def __init__(self, contents: str, type: str, album_id: Optional[int], artist_id: Optional[int], page: Optional[int]):
        self.album_id = album_id  # album id
        self.artist_id = artist_id  # artist_id
        self.contents = contents
        self.type = type  # artist or album
        self.page = 1 if not page else page
        if album_id:
            self.url = f"https://www.music-flo.com/api/meta/v1/{self.contents}/{self.album_id}/{self.type}"
        else:
            self.url = f"https://www.music-flo.com/api/meta/v1/{self.contents}/{self.artist_id}/{self.type}"
        if self.contents == 'artist':
            if self.type == 'track':
                self.url += f'?sortType=POPULARITY&page={self.page}&size=30&roleType=ALL'
            else:
                self.url += f'?sortType=RECENT&page={self.page}&size=30&roleType=RELEASE'
        self.user_agent = random.choice(self.USER_AGENT_LIST)
        self.headers = {
            'User-Agent': self.user_agent
        }
        self.music_data_list = []

    @staticmethod
    def get_best_quality_of_image(img_list: List) -> AnyStr:
        for img in img_list:
            if img['size'] == 1000:
                return img['url']
        # Todo: If can't find image what size is 1000, return max size image
        return None

    def parse_data(self):
        res = requests.get(self.url, headers=self.headers)
        json_result = json.loads(res.text)
        success = True if json_result['code'] == '2000000' else False  # response status check

        self.music_data_list = json_result['data']['list']

        return success, self.music_data_list

    def get_data(self):
        success, music_data_list = self.parse_data()

        search_result_list = []

        if success:
            for music_data in music_data_list:
                data = None
                if self.type == 'track':
                    data = self.make_track_response_data(music_data)
                elif self.type == 'album':
                    data = self.make_album_response_data(music_data)

                search_result_list.append(data)

            return search_result_list

    def make_track_response_data(self, music_data):
        song_title = music_data['name']
        album_id = music_data['album']['id']
        album_image = self.get_best_quality_of_image(music_data['album']['imgList'])
        artist_id = music_data['artistList'][0]['id']
        artist_name = music_data['artistList'][0]['name']
        try:
            title_yn = True if music_data['titleYn'] == 'Y' else False

            return {
                'song_title': song_title,
                'album_id': album_id,
                'image_url': album_image,
                'artist_id': artist_id,
                'artist_name': artist_name,
                'title_yn': title_yn,
            }
        except KeyError:
            return {
                'song_title': song_title,
                'album_id': album_id,
                'image_url': album_image,
                'artist_id': artist_id,
                'artist_name': artist_name,
            }

    def make_album_response_data(self, music_data):
        album_title = music_data['title']
        album_id = music_data['id']
        artist_id = music_data['artistList'][0]['id']
        artist_name = music_data['artistList'][0]['name']
        album_image = self.get_best_quality_of_image(music_data['imgList'])
        release_date = music_data['releaseYmd']

        return {
            'album_title': album_title,
            'album_id': album_id,
            'artist_id': artist_id,
            'artist_name': artist_name,
            'album_image': album_image,
            'release_date': datetime.strptime(release_date, '%Y%m%d').strftime('%Y.%m.%d'),
        }
