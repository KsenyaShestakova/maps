import os
import sys
from io import BytesIO

import pygame as pygame
import requests
from PIL import Image

pygame.init()


def load_image(name, colorkey=None):
    fullname = name
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


API_KEY_GEOCODER = "40d1649f-0493-4b70-98ba-98533de7710b"
geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"
map_api_server = "http://static-maps.yandex.ru/1.x/"

geocoder_params = {
    "apikey": API_KEY_GEOCODER,
    "geocode": 'Австралия',
    "format": "json"}

response = requests.get(geocoder_api_server, params=geocoder_params)

if response:
    json_response = response.json()
else:
    raise RuntimeError(f'''Ошибка выполнения запроса: {response.url}\nHTTP статус:{response.status_code}({response.reason})''')

toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
toponym_coodrinates = toponym["Point"]["pos"]
toponym_longitude, toponym_lattitude = toponym_coodrinates.split(" ")

ll = ",".join([toponym_longitude, toponym_lattitude])

envelope = toponym['boundedBy']['Envelope']
l, b = envelope['lowerCorner'].split(' ')
r, t = envelope['upperCorner'].split(' ')
dx, dy = abs(float(l) - float(r)) / 2, abs(float(t) - float(b)) / 2
spn = ','.join([str(dx), str(dy)])


map_params = {
    "ll": ll,
    "spn": spn,
    "l": "sat,skl"
}

response = requests.get(map_api_server, params=map_params)
map_file = "map.png"
with open(map_file, "wb") as file:
    file.write(response.content)

size = height, width = 600, 450
screen = pygame.display.set_mode(size)
image = load_image('map.png')
screen.blit(image, (0, 0))
pygame.display.flip()
while pygame.event.wait().type != pygame.QUIT:
    pass
pygame.quit()

os.remove(map_file)