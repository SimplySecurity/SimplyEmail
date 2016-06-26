# !/usr/bin/env python

# Class will have the following properties:
# 1) name / description
# 2) main name called "ClassName"
# 3) execute function (calls everything it needs)
# 4) places the findings into a queue
import configparser
import requests
import time
import logging
from Helpers import Download
from Helpers import helpers
from Helpers import Parser
from bs4 import BeautifulSoup


class ClassName(object):

    def __init__(self, Domain, verbose=False):
        self.apikey = False
        self.name = "PasteBin Search for Emails"
        self.description = "Uses pastebin to search for emails, parses them out of the"
        config = configparser.ConfigParser()
        try:
            self.logger = logging.getLogger("SimplyEmail.PasteBinSearch")
            config.read('Common/SimplyEmail.ini')
            self.Domain = Domain
            self.Quanity = int(config['GooglePasteBinSearch']['StartQuantity'])
            self.UserAgent = {
                'User-Agent': helpers.getua()}
            self.Limit = int(config['GooglePasteBinSearch']['QueryLimit'])
            self.Counter = int(config['GooglePasteBinSearch']['QueryStart'])
            self.verbose = verbose
            self.urlList = []
            self.Text = ""
        except Exception as e:
            self.logger.critical(
                'PasteBinSearch module failed to __init__: ' + str(e))
            print helpers.color("[*] Major Settings for PasteBinSearch are missing, EXITING!\n", warning=True)

    def execute(self):
        self.logger.debug("PasteBinSearch started")
        self.search()
        FinalOutput, HtmlResults, JsonResults = self.get_emails()
        return FinalOutput, HtmlResults, JsonResults

    def search(self):
        dl = Download.Download(self.verbose)
        while self.Counter <= self.Limit and self.Counter <= 100:
            time.sleep(1)
            if self.verbose:
                p = ' [*] Google Search for PasteBin on page: ' + \
                    str(self.Counter)
                self.logger.info(
                    "GooglePasteBinSearch on page: " + str(self.Counter))
                print helpers.color(p, firewall=True)
            try:
                url = "http://www.google.com/search?num=" + str(self.Quanity) + "&start=" + str(self.Counter) + \
                      '&hl=en&meta=&q=site:pastebin.com+"%40' + \
                    self.Domain + '"'
            except Exception as e:
                error = " [!] Major issue with Google Search for PasteBin:" + \
                    str(e)
                self.logger.error(
                    "GooglePasteBinSearch could not create URL: " + str(e))
                print helpers.color(error, warning=True)

            try:
                r = requests.get(url, headers=self.UserAgent)
            except Exception as e:
                error = " [!] Fail during Request to PasteBin (Check Connection):" + str(
                    e)
                self.logger.error(
                    "Fail during Request to PasteBin (Check Connection): " + str(e))
                print helpers.color(error, warning=True)
            try:
                RawHtml = r.content
                try:
                    # check for captcha in the source
                    dl.GoogleCaptchaDetection(RawHtml)
                except Exception as e:
                    self.logger.error("Issue checking for captcha: " + str(e))
                soup = BeautifulSoup(RawHtml, "lxml")
                for a in soup.select('.r a'):
                    # remove urls like pastebin.com/u/Anonymous
                    if "/u/" not in str(a['href']):
                        self.urlList.append(a['href'])
            except Exception as e:
                error = " [!] Fail during parsing result: " + str(e)
                self.logger.error(
                    "PasteBinSearch Fail during parsing result: " + str(e))
                print helpers.color(error, warning=True)
            self.Counter += 100
        # Now take all gathered URL's and gather the Raw content needed
        for Url in self.urlList:
            try:
                Url = "http://pastebin.com/raw/" + str(Url).split('/')[3]
                data = requests.get(Url, timeout=2)
                self.Text += data.content
            except Exception as e:
                error = "[!] Connection Timed out on PasteBin Search:" + str(e)
                self.logger.error(
                    "Connection Timed out on PasteBin raw download: " + str(e))
                print helpers.color(error, warning=True)

        if self.verbose:
            p = ' [*] Searching PasteBin Complete'
            self.logger.info("Searching PasteBin Complete")
            print helpers.color(p, firewall=True)

    def get_emails(self):
        Parse = Parser.Parser(self.Text)
        Parse.genericClean()
        Parse.urlClean()
        FinalOutput = Parse.GrepFindEmails()
        HtmlResults = Parse.BuildResults(FinalOutput, self.name)
        JsonResults = Parse.BuildJson(FinalOutput, self.name)
        self.logger.debug("PasteBinSearch completed search")
        return FinalOutput, HtmlResults, JsonResults
