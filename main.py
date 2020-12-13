"""
MyIDM: Python multithreaded CLI download manager
Author: Shann Aurelle Ripalda
Date of last revision: December 2, 2020
Description: A download accelerator for all platforms. It runs
             in the console.
Roadmap: Show the speed of the connection. Download files in a priority queue.
"""
# Multi purpose downloader script from ade@pipe-devnull.com
# Code is from a rewrite to Python 3 from Python 2.7 by Fausan Elka
# Edited time.clock() to time.perf_counter() from source code

""" Import """
import sys
import os
import time
from threading import Thread
from queue import Queue
import argparse
import binascii
import urllib.request
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
import simplejson as json


display_on_console = print

def display_download_details(inputfile,output_directory,flist):
    print("----------pydownload----------------")
    print("------------------------------------")
    print("JSON file:             {0}".format(inputfile))
    print("Output Directory:      {0}".format(output_directory))
    print("File list:             {0}".format(flist))
    print("------------------------------------")
 
class Downloader(Thread):
    """ Downloader class - reads queue and downloads each file in succession """
    def __init__(self, queue, output_directory):
        Thread.__init__(self, name=binascii.hexlify(os.urandom(16)))
        self.queue = queue
        self.output_directory = output_directory
 
    def run(self):
        while True:
            # gets the url from the queue
            url = self.queue.get()
            # download the file
            display_on_console("* Thread {0} - processing URL".format(self.name))
            self.download_file(url)
            # send a signal to the queue that the job is done
            self.queue.task_done()
 
    def download_file(self, url):
        """ download file """
        t_start = time.perf_counter()
        r = requests.get(url, timeout=0.01)

        # If the connection to the server is OK, start downloading the file
        # HTTP Status Code 200 means OK 
        if r.status_code == 200:
            t_elapsed = time.perf_counter() - t_start
            display_on_console("* Thread: {0} Downloaded {1} in {2} seconds".format(self.name, url, str(t_elapsed)))
            fname = self.output_directory + '/' + os.path.basename(urllib.request.unquote(url))
            with open(fname, 'wb') as out:
                out.write(r.content)

        else:
            display_on_console("* Thread: {0} Bad URL: {1}".format(self.name, url))
 
class DownloadManager():
    """ Spawns dowloader threads and manages URL downloads queue """
    def __init__(self, download_dict, output_directory, thread_count=4):
        self.thread_count = thread_count
        self.download_dict = download_dict
        self.output_directory = output_directory
 
    def begin_downloads(self):
        """
        Start the downloader threads, fill the queue with the URLs and\n
        then feed the threads URLs via the queue
        """
        queue = Queue()

        # Create a thread pool and give them a queue
        for i in range(self.thread_count):
            t = Downloader(queue, self.output_directory)
            t.daemon = True
            t.start()

        # Load the queue from the download dict
        for linkname in self.download_dict:
            queue.put(self.download_dict[linkname])

        # Wait for the queue to finish
        queue.join()
        return
 
parser = argparse.ArgumentParser()
parser.usage = "pydownload.py -o <OutputDirectory> -i <JSONinputfile> -f <url1,url2,url3>"
# -o represents output file
# -i represent the json input file
# -f represents the string URLs separated by comma
parser.add_argument('-o', '--output')
parser.add_argument('-i', '--ifile')
parser.add_argument('-f', '--flist')
 
def main(argv):
    """ Execute """
    inputfile = None
    flist = None

    if argv.output:
        output_directory = argv.output

    else:
        display_on_console(parser.usage)
        sys.exit(2)

    if argv.ifile:
        inputfile = argv.ifile

    elif argv.flist:
        flist = argv.flist.split(',')

    display_download_details(inputfile,output_directory,flist)

    download_dict = {}

    if inputfile is not None:
        fp = open(inputfile)
        url_list = json.load(fp)
        for url in url_list:
            download_dict[url['link_name']] = url['link_address']

    if flist is not None:
        for f in flist:
            download_dict[str(f)] = f

    if not download_dict:
        print("* No URLS to download, got the usage right?")
        print("USAGE: " + parser.usage)
        sys.exit(2)

    download_manager = DownloadManager(download_dict, output_directory, 4)
    download_manager.begin_downloads()
 
if __name__ == '__main__':
    args = parser.parse_args()
    main(args)