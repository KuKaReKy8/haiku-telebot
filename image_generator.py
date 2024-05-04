import json
import os
import time
from dotenv import *
import base64
import requests


class Text2ImageAPI:

    def __init__(self, url, api_key, secret_key):
        self.URL = url
        self.AUTH_HEADERS = {
            'X-Key': f'Key {api_key}',
            'X-Secret': f'Secret {secret_key}',
        }

    def get_model(self):
        response = requests.get(self.URL + 'key/api/v1/models', headers=self.AUTH_HEADERS)
        data = response.json()
        return data[0]['id']

    def generate(self, prompt, model, images=1, width=1920, height=1024):
        params = {
            "type": "GENERATE",
            "numImages": images,
            "width": width,
            "height": height,
            "generateParams": {
                "query": f"Иллюстрация для японского стихотворения хайку в стиле азиатской средневековой живопоси, \
                        текст хайку такой: {prompt}; выское качество"
            }
        }

        data = {
            'model_id': (None, model),
            'params': (None, json.dumps(params), 'application/json')
        }
        response = requests.post(self.URL + 'key/api/v1/text2image/run', headers=self.AUTH_HEADERS, files=data)
        data = response.json()
        return data['uuid']

    def check_generation(self, request_id, attempts=10, delay=10):
        while attempts > 0:
            response = requests.get(self.URL + 'key/api/v1/text2image/status/' + request_id, headers=self.AUTH_HEADERS)
            data = response.json()
            if data['status'] == 'DONE':
                return data['images']

            attempts -= 1
            time.sleep(delay)

def make_image(prompt):
    load_dotenv(find_dotenv())
    api = Text2ImageAPI('https://api-key.fusionbrain.ai/', os.environ.get('API_KEY'), os.environ.get('API_SECRET_KEY'))
    model_id = api.get_model()
    uuid = api.generate(prompt, model_id)
    image = api.check_generation(uuid)[0]
    image_decoded = base64.b64decode(image)
    num = len(os.listdir('images'))
    path = f'images/image{num}.jpg'
    with open(path, 'wb') as file:
        file.write(image_decoded)
    return image_decoded, path


if __name__ == '__main__':
    load_dotenv(find_dotenv())
    api = Text2ImageAPI('https://api-key.fusionbrain.ai/', os.environ.get('API_KEY'), os.environ.get('API_SECRET_KEY'))
    model_id = api.get_model()
    uuid = api.generate("Даже старый дырявый пол, куст барбариса - скворца над кошкой", model_id)
    image = api.check_generation(uuid)[0]
    image_decoded = base64.b64decode(image)



