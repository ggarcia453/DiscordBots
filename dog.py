from OpenWeather import _download_url
import random

class Dog:
    def __init__(self, breed):
        self.breed = breed
        self._url_r = 'https://dog.ceo/api/breeds/image/random'
        if breed is not None:
            self._url_b = f'https://dog.ceo/api/breed/{self.breed.lower()}/images'

    def dog_pic(self):
        if self.breed is None:
            data = _download_url(self._url_r)
            if data is not None and 'status' in data.keys() and data['status'] == 'success':
                return data['message']
            else:
                return 'Could not find images :('
        elif type(self.breed) == str:
            self.breed = self.breed.lower()
            self._url_b = f'https://dog.ceo/api/breed/{self.breed}/images'
            data = _download_url(self._url_b)
            if data is not None and 'message' in data.keys():
                num = random.randint(0, len(data))
                return data['message'][num]
            else:
                return 'Could not find images :('





