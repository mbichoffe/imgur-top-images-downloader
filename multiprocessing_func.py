#!/usr/bin/env python3
"""
To use multiple processes we create a multiprocessing Pool.
With the map method it provides, we will pass the list of URLs to the pool,
which in turn will spawn 8 new processes and use each one to download
the images in parallel. This is true parallelism, but it comes with a cost.
The entire memory of the script is copied into each subprocess that is spawned.
"""
import logging
import os
from functools import partial
from multiprocessing.pool import Pool
from time import time
from os.path import join, dirname
from dotenv import load_dotenv, find_dotenv

from download import setup_download_dir, get_links, download_link


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
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
    links = get_links(client_id)
    # With functools.partial, default values will start replacing variables
    # from the left. So the download_link function (first arg in partial) will
    # take in the download dir as directory arg for all links in the mapping
    # below
    download = partial(download_link, download_dir)
    # map(function_to_apply, list_of_inputs)
    with Pool(8) as p:
        p.map(download, links)
    logging.info('Took %s seconds', time() - ts)

if __name__ == '__main__':
    main()
