#!/usr/bin/env python3
import logging
import os
from dotenv import load_dotenv, find_dotenv
from os.path import join, dirname
from time import time
from download import setup_download_dir, get_links, download_link

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logging.getLogger('requests').setLevel(logging.CRITICAL)
logger = logging.getLogger(__name__)
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

def main():
    ts = time()
    client_id = os.environ.get('IMGUR_CLIENT_ID')
    if not client_id:
        raise Exception("Couldn't find IMGUR_CLIENT_ID environment variable!")
    download_dir = setup_download_dir()
    logger.info('new dir: {}'.format(download_dir))
    links = [l for l in get_links(client_id) if l.endswith('.jpg')]
    for link in links:
        download_link(download_dir, link)
    print('Took {}s'.format(time() - ts))

if __name__ == '__main__':
    main()
