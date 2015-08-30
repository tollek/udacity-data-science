#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup


MAGICZNY_KRAKOW_HTM = 'magiczny_krakow.htm'
RESTAURANTS_LIST = 'restaurants.txt'


def extract_magiczny_krakow(magiczny_krakow_htm):
    html_doc = open(magiczny_krakow_htm, 'r')
    soup = BeautifulSoup(html_doc, 'html.parser')
    rest_table = soup.find_all(id="rest_res")
    if len(rest_table) != 1:
        raise Exception("too many #rest_res")
    rest_body = rest_table[0].find_all('tbody')
    if len(rest_body) != 1:
        raise Exception("too many #rest_res.tbody")

    restaurants = []
    for row in rest_body[0].find_all('tr'):
        first_cell = row.find('td')
        rest_name = first_cell.text
        rest_name = clean_restaurant_name(rest_name)
        restaurants.append(rest_name)
    return restaurants

def clean_restaurant_name(name):
    name = name.strip()
    for remove_prefix in [
        'Restauracja ',
        'Restrauracja ',
        'Restauracja/Winiarnia ',
        'Restauracja/Bar ',
        'Restauracja-Drink Bar ',
        'Restauracja-Kawiarnia ',
        'Restauracja/Pizzeria ',
        'Restauracja/Resto ',
        'Trattoria ',
        'Pizzeria ',
    ]:
        if name.startswith(remove_prefix):
            name = name[len(remove_prefix):]

    for remove_suffix in [
        ' Restaurant&Cafe',
        ' Restaurant',
        ' Bar',
        ' Restobar',
        ' Restaur',
        ' Restaura',

    ]:
        if name.endswith(remove_suffix):
            name = name[:len(remove_suffix)]


    manual_fixings = {
        'Kompania Kuflowa Pod Wawelem': 'Pod Wawelem',
        'Kremówka z Cocktail-baru Czarodziej': 'Czarodziej',
        'w Willi Decjusza': 'Willa Decjusza',
        'Dali Club&Lunch Bar Cafe': 'Dali Club',
        'Grecka Tawerna Hellada': 'Hellada',
        'Anturium (Crown Piast Hotel&Park)': 'Anturium',
        'Gehanowska Pod Słońcem': 'Pod Słońcem',
        'Hamsa Hummus & Happiness Isreali Restobar': 'Hamsa Hummus',
        'i Oranżeria Augusta': 'Oranżeria Augusta',
        'Indyjska Indus Tandoor': 'Tandoor',
        'Magnifica (Hotel Farmona)': 'Magnifica',
        'Meho Cafe Bar & Garden': 'Meho',
        'Meksykańska Alebriche': 'Alebriche',
        'Orientalna Mekong': 'Mekong',
        'Resto-Bar-Gallery Zielone Tarasy': 'Zielone Tarasy',
        'Stara Zajezdnia Kraków by de Silva': 'Stara Zajezdnia',
        'Sznycel olbrzym z Kompani Kuflowej "Pod Wawelem"': 'Pod Wawelem',
        'Śledzie z Ambasady Śledzia': 'Ambasada Śledzia',
        'Torty z Galerii Tortów Artystycznych': 'Galeria Tortów Artystycznych',
        'Zapiekanki u Endziora': 'U Endziora',
    }
    if name in manual_fixings:
        name = manual_fixings[name]

    return name

def dump_restaurants(restaurants, output_file):
    f = open(output_file, 'w')
    data = u'\n'.join(restaurants).encode('utf-8')
    f.write(data)
    f.write(u'\n')
    f.close()

def load_restaurants(rest_file):
    f = open(rest_file, 'r').readlines()
    f = [x.decode('utf-8')[:-1] for x in f]
    return f


if __name__ == '__main__':
    restaurants = extract_magiczny_krakow(MAGICZNY_KRAKOW_HTM)
    dump_restaurants(restaurants, RESTAURANTS_LIST)
