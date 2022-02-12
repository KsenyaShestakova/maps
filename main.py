import os
import sys
from io import BytesIO

import pygame as pygame
import requests
from PIL import Image

pygame.init()

API_KEY_GEOCODER = "40d1649f-0493-4b70-98ba-98533de7710b"


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


def get_map(ll, map_type="map", add_params=None):
    map_params = {
        "ll": ll,
        "l": map_type
    }

    if isinstance(add_params, dict):
        map_params.update(add_params)

    map_api_server = "http://static-maps.yandex.ru/1.x/"

    response = requests.get(map_api_server, params=map_params)
    return response


d, sh, m = input(), input(), int(input())
coords = f'{d},{sh}'
response = get_map(coords, add_params={"z": f"{m}"})

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