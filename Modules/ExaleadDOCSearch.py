# !/usr/bin/env python

# Class will have the following properties:
# 1) name / description
# 2) main name called "ClassName"
# 3) execute function (calls everthing it neeeds)
# 4) places the findings into a queue

import configparser
import requests
import time
import re
import urlparse
import os
from Helpers import Download
from Helpers import helpers
from Helpers import Parser
from bs4 import BeautifulSoup
from subprocess import Popen, PIPE
from cStringIO import StringIO

# import for "'ascii' codec can't decode byte" error
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
# import for "'ascii' codec can't decode byte" error


class ClassName:

    def __init__(self, Domain, verbose=False):
        self.apikey = False
        self.name = "Exalead DOC Search for Emails"
        self.description = "Uses Exalead Dorking to search DOCs for emails"
        config = configparser.ConfigParser()
        try:
            config.read('Common/SimplyEmail.ini')
            self.Domain = Domain
            self.Quanity = int(config['ExaleadDOCSearch']['StartQuantity'])
            self.UserAgent = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
            self.Limit = int(config['ExaleadDOCSearch']['QueryLimit'])
            self.Counter = int(config['ExaleadDOCSearch']['QueryStart'])
            self.verbose = verbose
            self.urlList = []
            self.Text = ""
        except:
            print helpers.color("[*] Major Settings for Exalead are missing, EXITING!\n", warning=True)

    def execute(self):
        self.search()
        FinalOutput, HtmlResults = self.get_emails()
        return FinalOutput, HtmlResults

    def convert_doc_to_txt(self, path):
        cmd = ['antiword', path]
        p = Popen(cmd, stdout=PIPE)
        stdout, stderr = p.communicate()
        return stdout.decode('ascii', 'ignore')

    def search(self):
        while self.Counter <= self.Limit and self.Counter <= 10:
            time.sleep(1)
            if self.verbose:
                p = '[*] Exalead DOC Search on page: ' + str(self.Counter)
                print helpers.color(p, firewall=True)
            try:
                url = 'http://www.exalead.com/search/web/results/?q="%40' + self.Domain + \
                      '"+filetype:word&elements_per_page=' + \
                    str(self.Quanity) + '&start_index=' + str(self.Counter)
            except Exception as e:
                error = "[!] Major issue with Exalead DOC Search: " + str(e)
                print helpers.color(error, warning=True)
            try:
                r = requests.get(url, headers=self.UserAgent)
            except Exception as e:
                error = "[!] Fail during Request to Exalead (Check Connection):" + str(
                    e)
                print helpers.color(error, warning=True)
            try:
                RawHtml = r.content
                # sometimes url is broken but exalead search results contain
                # e-mail
                self.Text += RawHtml
                soup = BeautifulSoup(RawHtml, "lxml")
                self.urlList = [h2.a["href"]
                                for h2 in soup.findAll('h4', class_='media-heading')]
            except Exception as e:
                error = "[!] Fail during parsing result: " + str(e)
                print helpers.color(error, warning=True)
            self.Counter += 30

        # now download the required files
        try:
            for url in self.urlList:
                if self.verbose:
                    p = '[*] Exalead DOC search downloading: ' + str(url)
                    print helpers.color(p, firewall=True)
                try:
                    filetype = ".doc"
                    dl = Download.Download(self.verbose)
                    FileName, FileDownload = dl.download_file(url, filetype)
                    if FileDownload:
                        if self.verbose:
                            p = '[*] Exalead PDF file was downloaded: ' + \
                                str(url)
                            print helpers.color(p, firewall=True)
                        self.Text += self.convert_doc_to_txt(FileName)
                except Exception as e:
                    error = "[!] Issue with opening DOC Files:%s\n" % (str(e))
                    print helpers.color(error, warning=True)
                try:
                    dl.delete_file(FileName)
                except Exception as e:
                    print e
        except:
            print helpers.color("[*] No DOC's to download from Exalead!\n", firewall=True)

        if self.verbose:
            p = '[*] Searching DOC from Exalead Complete'
            print helpers.color(p, status=True)

    def get_emails(self):
        Parse = Parser.Parser(self.Text)
        Parse.genericClean()
        Parse.urlClean()
        FinalOutput = Parse.GrepFindEmails()
        HtmlResults = Parse.BuildResults(FinalOutput, self.name)
        return FinalOutput, HtmlResults
