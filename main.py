import os
import sys
import pygame as pygame
import requests

pygame.init()

API_KEY_GEOCODER = "40d1649f-0493-4b70-98ba-98533de7710b"
API_KEY_SEARCH = 'dda3ddba-c9ea-4ead-9010-f43fbc15c6e3'


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


def find_organizations(ll, spn, request, lang="ru_RU"):
    search_api_server = "https://search-maps.yandex.ru/v1/"
    search_params = {
        "apikey": API_KEY_SEARCH,
        "text": request,
        "ll": ll,
        "spn": spn,
        "lang": lang
    }
    response = requests.get(search_api_server, params=search_params)
    if response:
        json_response = response.json()
    else:
        raise RuntimeError(
            f"""Ошибка выполнения запроса: {response.url}\nHTTP статус: {response.status_code}({response.reason})""")
    organizations = json_response["features"]

    return organizations


def find_nearest_organization(ll, spn, request, lang="ru_RU"):
    organizations = find_organizations(ll, spn, request, lang)
    if len(organizations):
        print(organizations[0])
        return organizations[0]


def get_index(geocode):
    geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"

    geocoder_params = {
        "apikey": API_KEY_GEOCODER,
        "geocode": geocode,
        "format": "json"}

    response = requests.get(geocoder_api_server, params=geocoder_params)

    if response:
        json_response = response.json()
    else:
        raise RuntimeError(
            f'''Ошибка выполнения запроса: {response.url}\nHTTP статус:{response.status_code}({response.reason})''')

    toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
    toponym_address = toponym["metaDataProperty"]["GeocoderMetaData"]["Address"]
    postal_code = toponym_address["postal_code"]
    return postal_code


if __name__ == '__main__':
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
    running = True
    while running:
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_PAGEDOWN:
                    m += 1
                    if m > 17:
                        m = 17
                    response = get_map(coords, add_params={"z": f"{m}"})
                    map_file = "map.png"
                    with open(map_file, "wb") as file:
                        file.write(response.content)
                    image = load_image('map.png')

                elif event.key == pygame.K_PAGEUP:
                    m -= 1
                    if m < 0:
                        m = 0
                    response = get_map(coords, add_params={"z": f"{m}"})
                    map_file = "map.png"
                    with open(map_file, "wb") as file:
                        file.write(response.content)
                    image = load_image('map.png')

        screen.blit(image, (0, 0))
        pygame.display.flip()

    pygame.quit()

    os.remove(map_file)