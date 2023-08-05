import requests
import sys
import re
from bs4 import BeautifulSoup
from .exception import *

GAME_URL = 'http://erogamescape.dyndns.org/~ap2/ero/toukei_kaiseki/game.php?game={0}'
POV_URL = 'http://erogamescape.dyndns.org/~ap2/ero/toukei_kaiseki/game_pov.php?game={0}'


def get_game(id):
    response = requests.get(GAME_URL.format(id))
    if response.status_code == 404:
        raise NotFoundError
    html = response.content
    soup = BeautifulSoup(html, 'lxml')
    game = {
        'id': id,
        'title': soup.find(id='game_title').get_text() if soup.find(id='game_title') is not None else None,
        'image': soup.find(id='main_image').find('img').get('src') if soup.find(id='main_image') is not None else None,
        'brand': soup.find(id='brand').find('a').get_text() if soup.find(id='brand') is not None else None,
        'sellday': soup.find(id='sellday').find('a').get_text() if soup.find(id='sellday') is not None else None,
        'genre': soup.find(id='erogame').find('td').get_text().strip().split('/') if soup.find(id='erogame') is not None else None,
        'median': soup.find(id='median').find('td').get_text() if soup.find(id='median') is not None else None,
        'average': soup.find(id='average').find('td').get_text() if soup.find(id='average') is not None else None,
        'count': soup.find(id='count').find('td').get_text() if soup.find(id='count') is not None else None,
        'stddev': soup.find(id='stddev').find('td').get_text() if soup.find(id='stddev') is not None else None,
        'max': soup.find(id='max').find('td').get_text() if soup.find(id='max') is not None else None,
        'min': soup.find(id='min').find('td').get_text() if soup.find(id='min') is not None else None,
        'giveup': soup.find(id='giveup').find('td').get_text() if soup.find(id='giveup') is not None else None,
        'tun': soup.find(id='tun').find('td').get_text() if soup.find(id='tun') is not None else None,
        'fun_time': soup.find(id='fun_time').find('td').get_text() if soup.find(id='fun_time') is not None else None,
        'play_time': soup.find(id='play_time').find('td').get_text() if soup.find(id='play_time') is not None else None,
        'sample_cg_list': [item.get('src') for item in soup.find(id='digiket_sample_cg_main').find_all('img')] if soup.find(id='digiket_sample_cg_main') is not None else None,
        'genga': [item.get_text() for item in soup.find(id='genga').find_all('a')] if soup.find(id='genga') is not None else None,
        'shinario': [item.get_text() for item in soup.find(id='shinario').find_all('a')] if soup.find(id='shinario') is not None else None,
        'seiyu': [item.get_text() for item in soup.find(id='seiyu').find_all('a')] if soup.find(id='seiyu') is not None else None,
    }

    response = requests.get(POV_URL.format(id))
    html = response.content
    soup = BeautifulSoup(html, 'lxml')
    game['pov'] = [item.get_text()
                   for item in soup.find(class_='coment').find_all('a', href=re.compile('povlist.php'))] if soup.find(class_='coment') is not None else []
    return game
