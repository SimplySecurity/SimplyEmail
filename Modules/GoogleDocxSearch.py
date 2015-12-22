#!/usr/bin/env python
# encoding=utf8 

# Class will have the following properties:
# 1) name / description
# 2) main name called "ClassName"
# 3) execute function (calls everthing it neeeds)
# 4) places the findings into a queue
import re
import requests
import urlparse
import os
import configparser
import requests
import docx2txt
import time
# from subprocess import Popen, PIPE
from Helpers import helpers
from Helpers import Parser
from BeautifulSoup import BeautifulSoup
from cStringIO import StringIO

class ClassName:

    def __init__(self, Domain, verbose=False):
        self.name = "Google DOCX Search for Emails"
        self.description = "Uses google Dorking to search for emails"
        config = configparser.ConfigParser()
        try:
            config.read('Common/SimplyEmail.ini')
            self.Domain = Domain
            self.Quanity = int(config['GoogleDocxSearch']['StartQuantity'])
            self.UserAgent = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
            self.Limit = int(config['GoogleDocxSearch']['QueryLimit'])
            self.Counter = int(config['GoogleDocxSearch']['QueryStart'])
            self.verbose = verbose
            self.urlList = []
            self.Text = ""
        except:
            print helpers.color("[*] Major Settings for GoogleDocxSearch are missing, EXITING!\n", warning=True)

    def execute(self):
        self.search()
        FinalOutput, HtmlResults = self.get_emails()
        return FinalOutput, HtmlResults


    def convert_docx_to_txt(self, path):
        # https://github.com/ankushshah89/python-docx2txt
        # Very simple setup of python-docx to text
        text = docx2txt.process(path)
        return unicode(text)


    def download_file(self, url):
        local_filename = url.split('/')[-1]
        # NOTE the stream=True parameter
        r = requests.get(url, stream=True)
        with open(local_filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=1024): 
                if chunk: # filter out keep-alive new chunks
                    f.write(chunk)
                    #f.flush() commented by recommendation from J.F.Sebastian
        return local_filename


    def search(self):
        while self.Counter <= self.Limit and self.Counter <= 100:
            time.sleep(1)
            if self.verbose:
                p = '[*] Google DOC Search on page: ' + str(self.Counter)
                print helpers.color(p, firewall=True)
            try:
                urly = "https://www.google.com/search?q=site:" + self.Domain + "+filetype:docx&start=" + str(self.Counter)
            except Exception as e:
                error = "[!] Major issue with Google Search:" + str(e)
                print helpers.color(error, warning=True)
            try:
                r = requests.get(urly)
            except Exception as e:
                error = "[!] Fail during Request to Google (Check Connection):" + \
                    str(e)
                print helpers.color(error, warning=True)
            RawHtml = r.content
            soup = BeautifulSoup(RawHtml)
            # I use this to parse my results, for URLS to follow
            for a in soup.findAll('a'):
                  try:
                    # https://stackoverflow.com/questions/21934004/not-getting-proper-links-
                    # from-google-search-results-using-mechanize-and-beautifu/22155412#22155412?
                    # newreg=01f0ed80771f4dfaa269b15268b3f9a9
                    l = urlparse.parse_qs(urlparse.urlparse(a['href']).query)['q'][0]
                    if l.startswith('http') or l.startswith('www'):
                      if "webcache.googleusercontent.com" not in l:
                        self.urlList.append(l)
                  except:
                    pass
            self.Counter += 10
        # now download the required files
        try:
            for url in self.urlList:
                if self.verbose:
                    p = '[*] Google DOC search downloading: ' + str(url)
                    print helpers.color(p, firewall=True)
                try:
                    FileName = self.download_file(url)
                    self.Text += self.convert_docx_to_txt(FileName)
                    # print self.Text
                except Exception as e:
                    print helpers.color("[!] Issue with Converting Docx Files\n", firewall=True)
                try:
                    os.remove(FileName)
                except Exception as e:
                    print e
        except:
          print helpers.color("[*] No DOC's to download from google!\n", firewall=True)

    def get_emails(self):
        Parse = Parser.Parser(self.Text)
        Parse.RemoveUnicode()
        Parse.genericClean()
        Parse.urlClean()
        # Unicode issues here:
        FinalOutput = Parse.GrepFindEmails()
        HtmlResults = Parse.BuildResults(FinalOutput,self.name)
        return FinalOutput, HtmlResults
