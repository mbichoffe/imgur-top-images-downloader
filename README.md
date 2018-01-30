# Concurrency and Parallelism in Python 🐍
This repository contains examples how to write code in Python that runs concurrently or in parallel. 
The scripts will download the most popular images on imgur to a _./images_ directory.

## Getting Started

The examples have been tested under Python 3.6.3 running on OS X.
If you are working with Python 2, the urllib has changed a lot between versions and you will need to update the `download.py` file accordingly. 

### Prerequisites
- [Register an application on imgur](https://api.imgur.com/oauth2/addclient) and get a client_id. On the registration page, select _'anonymous usage without user authorization'_ to avoid 'bad request' and 'permission denied' errors when making requests to the API.
- For the _redis_queue.py_ example you will also need to be running a redis server.  This [quickstart](https://redis.io/topics/quickstart) will show you how to install and configure redis.  If you are using a Mac OSX, use Homebrew or `curl` instead of `wget`.

### Installing
Create a Pyton3 based virtual environment:
```sh
virtualenv -p python3 env
```
Set into the virtual environment:
```sh
source env/bin/activate
```
Clone the repository to your current directory:
```sh
$ git clone https://github.com/mbichoffe/imgur-top-images-downlodader.git
$ cd imgur-top-images-downloader/
```
Install dependencies:
```sh
$ pip install -r requirements.txt
```
Rename .env_example as .env:
```sh
$ mv .env_example .env
```
Don't forget to add your own client id to the `.env` file!

Run an example file - the script will download and save files to your disk and output the amount of time it took to download the images: 
```sh
$ python threading_func.py 
2018-01-29 18:54:09,659 - __main__ - INFO - Queueing https://i.imgur.com/OK1mkCJ.png
2018-01-29 18:54:09,659 - __main__ - INFO - Queueing https://i.imgur.com/G6lVMQW.png
2018-01-29 18:54:09,968 - download - INFO - Downloaded https://i.imgur.com/G6lVMQW.png
2018-01-29 18:54:10,135 - download - INFO - Downloaded https://i.imgur.com/OK1mkCJ.png
2018-01-29 18:54:10,135 - root - INFO - Took 0.7053031921386719
```
There are currently four examples on this repository:
* `single.py` - Naive implementation, downloads one file at a time. It works perfectly fine if you just need to download a small number of images.

* `threading_func.py` - Creates a pool of 8 threads, making a total of 9 threads including the main thread. 
    Check out the [threading docs](https://docs.python.org/3/library/threading.html) and this [tutorial](https://pythonprogramming.net/threading-tutorial-python/) to learn more.
Threads are lighter than processes, and share the same memory space. This script ran 5x faster than `single.py` on my computer.
Only one thread is executed at a time using this process, due to CPython's global interpreter lock. Therefore, the code is concurrent, but not parallel. 
Because downloading the images is an IO bound task, threading gives a large speed increase, but that is not always the case. If your script performs CPU bound tasks (crunching numbers or unzipping files), then multithreading can result in slower execution time.

* `multiprocessing_func.py` - this script creates a multiprocessing Pool. With the map method it provides, we will pass the list of URLs to the pool, which in turn will spawn 8 new processes and use each one to download the images in parallel. The [official documentation](https://docs.python.org/2/library/multiprocessing.html) is quite easy to digest.
Multiprocessing is a better choice if your code is CPU bound, and it is easier to implement. But the entire memory of the script is copied into each subprocess it spawns. It does not make a lot of difference for this use case, but it can become costly in larger applications.

* `redis-queue.py` - Redis Queue is 'a simple Python library for queueing jobs and processing them in the background with workers.' 
This is useful if you have long-running back-end tasks (a script that is executed periodically by a worker process) for web applications. You can have those tasks in another machine (or multiple machines).
You first enqueue a function and its arguments using the library. This [pickles](https://docs.python.org/3.4/library/pickle.html) the function call representation, which is then appended to a Redis list. 
Then at least one worker will need to be listening on that job queue for something to happen. 
To run this example (`redis-queue.py`), you will need to:
    - Run a redis server 
        ```sh
        $ redis-server
        ```
    - Open a new terminal and set up a worker, using RQ's script to listen on the default queue:
        ```sh
        $ rqworker
        ```
    Please make sure your current working directory is the same as where the scripts reside in. If you want to listen to a different queue, you can run “rqworker queue_name” and it will listen to that named queue. 

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* This [Toptal blog post](http://www.toptal.com/python/beginners-guide-to-concurrency-and-parallelism-in-python) by Marcus McCurdy is where most of this code came from. 