#!/usr/bin/env python
import requests
import os
import configparser
import helpers
import logging
import urllib2
import time
from bs4 import BeautifulSoup
from random import randint


class Download(object):

    def __init__(self, verbose=False):
        config = configparser.ConfigParser()
        try:
            self.logger = logging.getLogger("SimplyEmail.Download")
            self.verbose = verbose
            config.read('Common/SimplyEmail.ini')
            self.UserAgent = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
        except Exception as e:
            print e

    def download_file(self, url, filetype, maxfile=100, verify=True):
        """
        Downloads a file using requests,

        maxfile=100 in MegaBytes
        chunk_size=1024 the bytes to write from mem
        """
        # using the filename is dangerous, could have UTF8 chars etc.
        local_filename = randint(10000, 999999999)
        # set name
        local_filename = str(local_filename) + str(filetype)
        # local_filename = url.split('/')[-1]
        # NOTE the stream=True parameter
        if url.startswith('http') or url.startswith('https'):
            pass
        else:
            url = 'http://' + str(url)
        try:
            time.sleep(2)
            self.logger.debug("Download started download: " + str(url))
            r = requests.get(url, stream=True, headers=self.UserAgent, verify=verify)
            with open(local_filename, 'wb+') as f:
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
            self.logger.error("Failed to download file: " + str(url) + ' error: ' + str(e))
            download = os.path.isfile(local_filename)
            return local_filename, download

    def download_file2(self, url, filetype, timeout=10):
        # using the filename is dangerous, could have UTF8 chars etc.
        local_filename = randint(10000, 999999999)
        # set name
        local_filename = str(local_filename) + str(filetype)
        # local_filename = url.split('/')[-1]
        # NOTE the stream=True parameter
        if url.startswith('http') or url.startswith('https'):
            pass
        else:
            # small hack till I figure out google cache errors
            url = 'http://' + str(url)
        try:
            self.logger.debug("Download2 started download: " + str(url))
            response = urllib2.urlopen(url, timeout=timeout)
            data = response.read()
            download = os.path.isfile(local_filename)
        except urllib2.HTTPError, e:
            self.logger.debug('urllib2 HTTPError: ' + e)
        except urllib2.URLError, e:
            self.logger.debug('urllib2 URLError: ' + e)
        except urllib2.HTTPException, e:
            self.logger.debug('urllib2 HTTPException: ' + e)
        except Exception as e:
            if self.verbose:
                p = ' [*] Download2 of file failed: ' + e
                print helpers.color(p, firewall=True)
            self.logger.error("Failed to download2 file: " + str(e))
        try:
            with open(local_filename, 'wb+') as f:
                f.write(data)
            download = os.path.isfile(local_filename)
            self.logger.debug("Download2 completed fully: " + str(url))
            return local_filename, download
        except:
            download = os.path.isfile(local_filename)
            return local_filename, download

    def delete_file(self, local_filename):
        # Deletes a file from local path
        try:
            if os.path.isfile(local_filename):
                os.remove(local_filename)
                self.logger.debug("File deleted: " + str(local_filename))
            else:
                if self.verbose:
                    p = ' [*] File not found to remove : ' + local_filename
                    print helpers.color(p, firewall=True)
        except Exception as e:
            self.logger.error("Failed to delete file: " + str(e))
            if self.verbose:
                print e

    def GoogleCaptchaDetection(self, RawHtml):
        soup = BeautifulSoup(RawHtml, "lxml")
        if "Our systems have detected unusual traffic" in soup.text:
            p = " [!] Google Captcha was detected! (For best results resolve/restart -- Increase sleep/jitter in SimplyEmail.ini)"
            self.logger.warning("Google Captcha was detected!")
            print helpers.color(p, warning=True)
            return True
        else:
            return False

    def requesturl(self, url, useragent, timeout=10, retrytime=5, statuscode=False, raw=False, verify=True):
        """
        A very simple request function
        This is setup to handle the following parms:

        url = the passed in url to request
        useragent = the useragent to use
        timeout = how long to wait if no "BYTES" rec

        Exception handling will also retry on the event of
        a timeout and warn the user.
        """
        rawhtml = ""
        try:
            r = requests.get(url, headers=self.UserAgent, timeout=timeout, verify=verify)
            rawhtml = r.content
            self.logger.debug(
                'Request completed: code = ' + str(r.status_code) + ' size = ' + str(len(rawhtml)) + ' url = ' + str(url))
        except requests.exceptions.Timeout:
            #  set up for a retry
            if self.verbose:
                p = ' [!] Request for url timed out, retrying: ' + url
                self.logger.info('Request timed out, retrying: ' + url)
                print helpers.color(p, firewall=True)
            r = requests.get(url, headers=self.UserAgent, timeout=retrytime, verify=verify)
            rawhtml = r.content
        except requests.exceptions.TooManyRedirects:
            # fail and move on, alert user
            if self.verbose:
                p = ' [!] Request for url resulted in bad url: ' + url
                self.logger.error(
                    'Request for url resulted in bad url: ' + url)
                print helpers.color(p, warning=True)
        except requests.exceptions.RequestException as e:
            # catastrophic error. bail.
            if self.verbose:
                p = ' [!] Request for url resulted in major error: ' + str(e)
                self.logger.critical(
                    'Request for url resulted in major error: ' + str(e))
                print helpers.color(p, warning=True)
        except Exception as e:
            p = ' [!] Request for url resulted in unhandled error: ' + str(e)
            self.logger.critical(
                'Request for url resulted in unhandled error: ' + str(e))
        # just return blank data if failed
        # to prevent bails
        if statuscode:
            # return status code and html
            status = r.status_code
            return rawhtml, status
        elif raw:
            # return raw request object
            return r
        else:
            return rawhtml
