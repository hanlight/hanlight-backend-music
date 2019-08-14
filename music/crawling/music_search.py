import requests, random, json
from bs4 import BeautifulSoup

from music.models import Album


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

    def __init__(self, param: str, type: str):
        self.param = param
        self.type = type
        self.url = f"http://search.api.mnet.com/search/{self.type}?q={self.param}"
        self.user_agent = random.choice(self.USER_AGENT_LIST)
        self.headers = {
            'User-Agent': self.user_agent
        }

    def parse_data(self):
        res = requests.get(self.url, headers=self.headers)
        json_result = json.loads(res.text)
        success = True if json_result['message'] == "성공" else False  # response status check
        music_data_list = json_result['data'][:10]

        return success, music_data_list

    def get_or_save_album_image(self, album_id: int, album_name: str, artist_name: str):
        try:
            album = Album.objects.get(album_id=album_id)
        except Album.DoesNotExist:
            url = f'http://www.mnet.com/album/{album_id}'

            res = requests.get(url, headers=self.headers)
            html = res.text
            soup = BeautifulSoup(html, 'html.parser')
            album_image_url = soup.select_one('#big_img_profile')['src']

            # Todo: Refactoring for bulk_create
            Album.objects.create(album_id=album_id, name=album_name, artist=artist_name, image_url=album_image_url)

            return album_image_url  # return album_image_url
        else:
            return album.image_url

    def get_data(self):
        success, music_data_list = self.parse_data()

        search_result_list = []

        if success:
            for music_data in music_data_list:
                song_name = music_data['songnm']
                album_name = music_data['albumnm']
                album_id = music_data['albumid']
                artist_name = music_data['artinfo'][0]['artistnm']

                album_image_url = self.get_or_save_album_image(album_id=album_id, album_name=album_name,
                                                               artist_name=artist_name)

                data = {
                    "song": song_name,
                    "album_id": int(album_id),
                    "album": album_name,
                    "artist": artist_name,
                    "image_url": album_image_url,
                }

                search_result_list.append(data)

            return search_result_list
