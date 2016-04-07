#!/usr/bin/env python
import requests
import os
import configparser
import helpers
from bs4 import BeautifulSoup
from random import randint


class Download(object):

    def __init__(self, verbose=False):
        config = configparser.ConfigParser()
        try:
            self.verbose = verbose
            config.read('Common/SimplyEmail.ini')
            self.UserAgent = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
        except Exception as e:
            print e

    def download_file(self, url, filetype):
        # using the filename is dangerous, could have UT8 chars etc.
        local_filename = randint(10000, 999999999)
        # set name
        local_filename = str(local_filename) + str(filetype)
        # local_filename = url.split('/')[-1]
        # NOTE the stream=True parameter
        try:
            r = requests.get(url, stream=True)
            with open(local_filename, 'wb') as f:
                for chunk in r.iter_content(chunk_size=1024):
                    if chunk:
                        # filter out keep-alive new chunks
                        f.write(chunk)
                        # f.flush() commented by recommendation from
                        # J.F.Sebastian
            download = os.path.isfile(local_filename)
            return local_filename, download
        except Exception as e:
            if self.verbose:
                p = ' [*] Download of file failed: ' + e
                print helpers.color(p, firewall=True)
            return local_filename, download

    def delete_file(self, local_filename):
        # Deletes a file from local path
        try:
            if os.path.isfile(local_filename):
                os.remove(local_filename)
            else:
                if self.verbose:
                    p = ' [*] File not found to remove : ' + local_filename
                print p
        except Exception as e:
            if self.verbose:
                print e

    def GoogleCaptchaDetection(self, RawHtml):
        soup = BeautifulSoup(RawHtml, "lxml")
        if "Our systems have detected unusual traffic" in soup.text:
            p = " [!] Google Captcha was detected! (For best results stop/resolve/restart)"
            print helpers.color(p, warning=True)
            return True
        else:
            return False
