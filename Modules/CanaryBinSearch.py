#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Non-API-Based
import requests
import configparser
import urllib2
from BeautifulSoup import BeautifulSoup
from Helpers import Parser
from Helpers import helpers

# Class will have the following properties:
# 1) name / description
# 2) main name called "ClassName"
# 3) execute function (calls everthing it neeeds)
# 4) places the findings into a queue

# This method will do the following:
# 1) Get raw HTML for lets say enron.com )
#    This is mainly do to the API not supporting code searched with out known repo or user
#    :(https://canary.pw/search/?q=earthlink.net&page=3)
# 2) Use beautiful soup to parse the results of the first (5) pages for <A HERF> tags that start with "/view/"
# 3) Ueses a list of URL's and places that raw HTML into a on value
# 4) Sends to parser for results

# Some considerations are the retunred results: max 100 it seems
# API may return a great array of results - This will be added later
# Still having some major python errors


class ClassName:

    def __init__(self, domain, verbose=False):
        self.name = "Searching Canary Paste Bin"
        self.description = "Search Canary for paste potential data dumps, this can take a bit but a great source"
        self.domain = domain
        config = configparser.ConfigParser()
        self.Html = ""
        try:
            config.read('Common/SimplyEmail.ini')
            self.Depth = int(config['CanaryPasteBin']['PageDepth'])
            self.Counter = int(config['CanaryPasteBin']['QueryStart'])
            self.verbose = verbose
        except:
            print helpers.color("[*] Major Settings for Canary PasteBin Search are missing, EXITING!\n", warning=True)

    def execute(self):
        self.process()
        FinalOutput, HtmlResults = self.get_emails()
        return FinalOutput, HtmlResults

    def process(self):
        # Get all the Pastebin raw items
        # https://canary.pw/search/?q=earthlink.net&page=3
        UrlList = []
        while self.Counter <= self.Depth:
            if self.verbose:
                p = '[*] Canary Search on page: ' + str(self.Counter)
                print helpers.color(p, firewall=True)
            try:
                url = "https://canary.pw/search/?q=" + str(self.domain) + "&page=" + \
                    str(self.Counter)
                r = requests.get(url, timeout=5)
                if r.status_code != 200:
                    break
            except Exception as e:
                error = "[!] Major issue with Canary Pastebin Search:" + str(e)
                print helpers.color(error, warning=True)
            RawHtml = r.content
            # Parse the results for our URLS)
            soup = BeautifulSoup(RawHtml)
            for a in soup.findAll('a', href=True):
                a = a['href']
                if a.startswith('/view'):
                    UrlList.append(a)
            self.Counter += 1
        # Now take all gathered URL's and gather the HTML content needed
        Status = "[*] Canary found " + str(len(UrlList)) + " PasteBin(s) to Search!"
        print helpers.color(Status, status=True)
        for item in UrlList:
            try:
                item = "https://canary.pw" + str(item)
                # They can be massive!
                rawhtml = urllib2.urlopen(item, timeout=20)
                try:
                    self.Html +=  rawhtml.read()
                except:
                    pass
            except Exception as e:
                error = "[!] Connection Timed out on Canary Pastebin Search:" + \
                    str(e)
                print helpers.color(error, warning=True)

    # We must Pre Parse (python dosnt like the large vars)
    def get_emails(self):
        # You must report back with parsing errors!!!
        # in one case I have seen alex@gmail.com:Password
        # This will break most Reg-Ex
        Parse = Parser.Parser(self.Html)
        Parse.genericClean()
        Parse.urlClean()
        FinalOutput = Parse.GrepFindEmails()
        HtmlResults = Parse.BuildResults(FinalOutput,self.name)
        return FinalOutput, HtmlResults
