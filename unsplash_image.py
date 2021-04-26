import random
import requests
from PIL import Image, ImageDraw, ImageFont
import click

AUTHORIZED_COLLECTION_IDS = [
    # GIRLS collections
    '234224',
    '1712483',
    '8909560',
    # LANDSCAPES
    # '9628327',
    # '496470',
    # '162232'
]

API_URL = "https://source.unsplash.com/collection"
DIMENSION = "1280x720"

def random_collection_id():
    return random.choice(AUTHORIZED_COLLECTION_IDS)

def download_img(collection_id):
    url = f"{API_URL}/{collection_id}/{DIMENSION}"
    im = Image.open(requests.get(url, stream=True).raw)
    return im

def get_approved_choice(im):
    im.show()
    if click.confirm('Do you want to use this image ?', default=True):
        print('This image is now used.')
        return True
    else:
        print('Image dropped. Let\'s try again !')
        return False
    

def get_random_picture():
    picture_found = False
    while not picture_found:
        collection_id = random_collection_id()
        im = download_img(collection_id)
        picture_found = get_approved_choice(im)
    return im


# print(get_random_picture())