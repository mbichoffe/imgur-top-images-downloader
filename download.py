#!/usr/bin/env python3
import logging
import os
import requests
from urllib.request import urlopen
from pathlib import Path

logger = logging.getLogger(__name__)

types = {'image/jpeg', 'image/png'}

def get_links(client_id):
    headers = {'Authorization': 'Client-ID ' + client_id}
    response = requests.get('https://api.imgur.com/3/gallery/random/random/', headers=headers)
    data = response.json()
    if response.ok:
        return [item['link'] for item in data['data'] if 'type' in item and item['type'] in types]
    else:
        logger.info('Error: {}'.format(data['error']))

def download_link(directory, link):
    download_path = directory / os.path.basename(link)
    with urlopen(link) as image, download_path.open('wb') as f:
        f.write(image.read())
    logger.info('Downloaded {}'.format(link))

def setup_download_dir():
    download_dir = Path('images')
    if not download_dir.exists():
        download_dir.mkdir()
    return download_dir
