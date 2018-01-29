#!/usr/bin/env python3

import logging
import os
from time import time
from os.path import join, dirname
from dotenv import load_dotenv, find_dotenv
from redis import Redis
from rq import Queue
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

    q = Queue(connection=Redis(host='localhost', port=6379))
    for link in links:
        logging.info('Here')
        # The enqueue method takes a function as its first argument, then any
        # other arguments or keyword arguments are passed along to that function
        # when the job is actually executed.
        # This pickles the function call representation,
        # which is then appended to a Redis list
        q.enqueue(download_link, download_dir, link)
    print('Took {}s'.format(time() - ts))

if __name__ == '__main__':
    main()