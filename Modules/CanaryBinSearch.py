#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Non-API-Based
import configparser
import logging
from BeautifulSoup import BeautifulSoup
from Helpers import Download
from Helpers import Parser
from Helpers import helpers

# Class will have the following properties:
# 1) name / description
# 2) main name called "ClassName"
# 3) execute function (calls everything it needs)
# 4) places the findings into a queue

# This method will do the following:
# 1) Get raw HTML for lets say enron.com )
#    This is mainly do to the API not supporting code searched with out known repo or user
#    :(https://canary.pw/search/?q=earthlink.net&page=3)
# 2) Use beautiful soup to parse the results of the first (5) pages for <A HREF> tags that start with "/view/"
# 3) Ueses a list of URL's and places that raw HTML into a on value
# 4) Sends to parser for results

# Some considerations are the retunred results: max 100 it seems
# API may return a great array of results - This will be added later
# Still having some major python errors


class ClassName(object):

    def __init__(self, domain, verbose=False):
        self.apikey = False
        self.name = "Searching Canary Paste Bin"
        self.description = "Search Canary for paste potential data dumps, this can take a bit but a great source"
        self.domain = domain
        config = configparser.ConfigParser()
        self.Html = ""
        try:
            self.UserAgent = {
                'User-Agent': helpers.getua()}
            self.logger = logging.getLogger("SimplyEmail.AskSearch")
            config.read('Common/SimplyEmail.ini')
            self.Depth = int(config['CanaryPasteBin']['PageDepth'])
            self.Counter = int(config['CanaryPasteBin']['QueryStart'])
            self.verbose = verbose
        except Exception as e:
            self.logger.critical(
                'CanaryBinSearch module failed to load: ' + str(e))
            print helpers.color("[*] Major Settings for Canary PasteBin Search are missing, EXITING!\n", warning=True)

    def execute(self):
        self.logger.debug("CanaryBinSearch module started")
        self.process()
        FinalOutput, HtmlResults = self.get_emails()
        return FinalOutput, HtmlResults

    def process(self):
        # Get all the Pastebin raw items
        # https://canary.pw/search/?q=earthlink.net&page=3
        UrlList = []
        dl = Download.Download(verbose=self.verbose)
        while self.Counter <= self.Depth:
            if self.verbose:
                p = ' [*] Canary Search on page: ' + str(self.Counter)
                self.logger.info(
                    "CanaryBinSearch on page: " + str(self.Counter))
                print helpers.color(p, firewall=True)
            try:
                url = "https://canary.pw/search/?q=" + str(self.domain) + "&page=" + \
                    str(self.Counter)
                rawhtml, statuscode = dl.requesturl(
                    url, useragent=self.UserAgent, statuscode=True)
                if statuscode != 200:
                    break
            except Exception as e:
                error = " [!] Major issue with Canary Pastebin Search:" + \
                    str(e)
                self.logger.error(
                    'Fail during Request to CanaryBinSearch (Check Connection): ' + str(e))
                print helpers.color(error, warning=True)
            # Parse the results for our URLS)
            soup = BeautifulSoup(rawhtml)
            for a in soup.findAll('a', href=True):
                a = a['href']
                if a.startswith('/view'):
                    UrlList.append(a)
            self.Counter += 1
        # Now take all gathered URL's and gather the HTML content needed
        Status = " [*] Canary found " + \
            str(len(UrlList)) + " CanaryBin(s) to Search!"
        self.logger.info(
            "CanaryBin found " + str(len(UrlList)) + " CanaryBin(s) to Search!")
        print helpers.color(Status, status=True)
        for item in UrlList:
            try:
                item = "https://canary.pw" + str(item)
                # They can be massive!
                rawhtml = dl.requesturl(
                    item, useragent=self.UserAgent, timeout=20)
                self.Html += rawhtml
            except Exception as e:
                error = " [!] Connection Timed out on Canary Pastebin Search:" + \
                    str(e)
                self.logger.error(
                    'Fail during Request to CanaryBinSearch bin (Check Connection): ' + str(e))
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
        HtmlResults = Parse.BuildResults(FinalOutput, self.name)
        self.logger.debug('CanaryBinSearch completed search')
        return FinalOutput, HtmlResults
