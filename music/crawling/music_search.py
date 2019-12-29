import requests
import random
import json

from datetime import datetime
from typing import List, Optional, AnyStr, Dict


class MusicSearch:
    USER_AGENT_LIST = [
        'Mozilla/5.0 (Linux; Android 4.4.2; XMP-6250 Build/HAWK) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/30.0.0.0 Safari/537.36 ADAPI/2.0 (UUID:9e7df0ed-2a5c-4a19-bec7-2cc54800f99d) RK3188-ADAPI/1.2.84.533 (MODEL:XMP-6250)',
        'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/11.1.2 Safari/605.1.15',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/602.4.8 (KHTML, like Gecko) Version/10.0.3 Safari/602.4.8',
        'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36 OPR/48.0.2685.52',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/603.3.8 (KHTML, like Gecko) Version/10.1.2 Safari/603.3.8',
    ]

    def __init__(self, keyword: str, type: str, page: Optional[int]):
        self.keyword = keyword  # 검색어
        self.type = type  # 검색 타입 ( 전체, 곡, 앨범, 아티스트 )
        self.page = 1 if not page else page
        if self.type:
            self.url = f"https://www.music-flo.com/api/search/v2/search/?keyword={self.keyword}&searchType={self.type}&page={self.page}&sortType=POPULAR&size=30"
        else:
            self.url = f"https://www.music-flo.com/api/search/v2/search/integration?keyword={self.keyword}"
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

        if success:
            if not self.type:
                detail = json_result['data']['list'][0]
                track = json_result['data']['list'][1]
                album = json_result['data']['list'][2]
                artist = json_result['data']['list'][3]
                self.music_data_list = [detail, track, album, artist, ]
            else:
                self.music_data_list = json_result['data']['list'][0]['list']

        return success, self.music_data_list

    def get_data(self):
        success, music_data_list = self.parse_data()

        search_result_list = []

        if success:
            if not self.type:
                detail = self.make_detail_response_data(music_data_list[0])
                track_music_list = []
                album_music_list = []
                artist_music_list = []

                if music_data_list[1]['type'] == 'TRACK':
                    for music_data in music_data_list[1]['list']:
                        data = self.make_track_response_data(music_data)
                        track_music_list.append(data)

                if music_data_list[2]['type'] == 'ALBUM':
                    for music_data in music_data_list[2]['list']:
                        data = self.make_album_response_data(music_data)
                        album_music_list.append(data)

                if music_data_list[3]['type'] == 'ARTIST':
                    for music_data in music_data_list[3]['list']:
                        data = self.make_artist_response_data(music_data)
                        artist_music_list.append(data)

                search_result_list = {
                    'detail': detail,
                    'track_list': track_music_list,
                    'album_list': album_music_list,
                    'artist_list': artist_music_list,
                }
            elif self.type == 'TRACK':
                for music_data in music_data_list:
                    data = self.make_track_response_data(music_data)

                    search_result_list.append(data)
            elif self.type == 'ALBUM':
                for music_data in music_data_list:
                    data = self.make_album_response_data(music_data)

                    search_result_list.append(data)
            elif self.type == 'ARTIST':
                for music_data in music_data_list:
                    data = self.make_artist_response_data(music_data)

                    search_result_list.append(data)
            else:
                return None

            return search_result_list
        else:
            return {
                'detail': dict(),
                'track_list': list(),
                'album_list': list(),
                'artist_list': list(),
            }

    def make_detail_response_data(self, music_data: dict) -> Dict:
        data = music_data['list'][0]
        if music_data['type'] == 'ARTIST':
            artist_name = data['name']
            artist_id = data['id']
            artist_group_type = data['artistGroupTypeStr']
            artist_image = self.get_best_quality_of_image(data['imgList'])

            return {
                'artist_name': artist_name,
                'artist_group_type': artist_group_type,
                'artist_id': artist_id,
                'image_url': artist_image,
            }
        elif music_data['type'] == 'TRACK':
            artist_name = data['artistList'][0]['name']
            album_title = data['album']['title']
            album_image = self.get_best_quality_of_image(data['album']['imgList'])
            album_id = data['id']
            track_title = data['name']

            return {
                'artist_name': artist_name,
                'album_title': album_title,
                'album_id': album_id,
                'track_title': track_title,
                'image_url': album_image,
            }
        elif music_data['type'] == 'ALBUM':
            track_title = data['title']
            album_id = data['id']
            artist_name = data['artistList'][0]['name']
            album_type = data['albumTypeStr']
            genre_style = data['genreStyle']
            release_date = data['releaseYmd']
            album_image = self.get_best_quality_of_image(data['imgList'])

            return {
                'track_title': track_title,
                'album_id': album_id,
                'artist_name': artist_name,
                'album_type': album_type,
                'genre_style': genre_style,
                'release_date': datetime.strptime(release_date, '%Y%m%d').strftime('%Y.%m.%d'),
                'image_url': album_image,
            }

    def make_track_response_data(self, music_data: dict) -> Dict:
        track_title = music_data['name']
        artist_id = music_data['artistList'][0]['id']
        artist_name = music_data['artistList'][0]['name']
        album_title = music_data['album']['title']
        album_id = music_data['album']['id']
        album_image = self.get_best_quality_of_image(music_data['album']['imgList'])

        return {
            'track_title': track_title,
            'artist_id': artist_id,
            'artist_name': artist_name,
            'album_title': album_title,
            'album_id': album_id,
            'image_url': album_image,
        }

    def make_album_response_data(self, music_data: dict) -> Dict:
        album_title = music_data['title']
        album_id = music_data['id']
        release_date = music_data['releaseYmd']
        artist_id = music_data['artistList'][0]['id']
        artist_name = music_data['artistList'][0]['name']
        album_image = self.get_best_quality_of_image(music_data['imgList'])

        return {
            'album_title': album_title,
            'album_id': album_id,
            'release_date': datetime.strptime(release_date, '%Y%m%d').strftime('%Y.%m.%d'),
            'artist_id': artist_id,
            'artist_name': artist_name,
            'image_url': album_image,
        }

    def make_artist_response_data(self, music_data: dict) -> Dict:
        artist_name = music_data['name']
        artist_id = music_data['id']
        artist_group_type = music_data['artistGroupTypeStr']
        artist_gender = music_data['sexCdStr']
        artist_image = self.get_best_quality_of_image(music_data['imgList'])

        return {
            'artist_name': artist_name,
            'artist_id': artist_id,
            'artist_group_type': artist_group_type,
            'artist_gender': artist_gender,
            'artist_image': artist_image,
        }
