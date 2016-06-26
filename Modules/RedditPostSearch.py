#!/usr/bin/env python

# Class will have the following properties:
# 1) name / description
# 2) main name called "ClassName"
# 3) execute function (calls everything it needs)
# 4) places the findings into a queue
import configparser
import time
import logging
from Helpers import Download
from Helpers import helpers
from Helpers import Parser


class ClassName(object):

    def __init__(self, Domain, verbose=False):
        self.apikey = False
        self.name = "RedditPost Search for Emails"
        self.description = "Uses RedditPosts to search for emails, and Parse the raw results ATM"
        config = configparser.ConfigParser()
        try:
            self.logger = logging.getLogger("SimplyEmail.RedditPostSearch")
            config.read('Common/SimplyEmail.ini')
            self.Domain = Domain
            self.UserAgent = {
                'User-Agent': helpers.getua()}
            self.Limit = int(config['RedditPostSearch']['QueryLimit'])
            self.Counter = int(config['RedditPostSearch']['QueryStart'])
            self.verbose = verbose
            self.Html = ""
        except Exception as e:
            self.logger.critical(
                'RedditPostSearch module failed to load: ' + str(e))
            print helpers.color(" [*] Major Settings for RedditPostSearch are missing, EXITING!\n", warning=True)

    def execute(self):
        self.logger.debug("RedditPostSearch started")
        self.search()
        FinalOutput, HtmlResults, JsonResults = self.get_emails()
        return FinalOutput, HtmlResults, JsonResults

    def search(self):
        dl = Download.Download(self.verbose)
        while self.Counter <= self.Limit and self.Counter <= 1000:
            time.sleep(1)
            if self.verbose:
                p = ' [*] RedditPost Search on result: ' + str(self.Counter)
                self.logger.debug(
                    "RedditPost Search on result: " + str(self.Counter))
                print helpers.color(p, firewall=True)
            try:
                url = "https://www.reddit.com/search?q=%40" + str(self.Domain) + \
                    "&restrict_sr=&sort=relevance&t=all&count=" + str(self.Counter) + \
                    '&after=t3_3mkrqg'
            except Exception as e:
                error = " [!] Major issue with RedditPost search:" + str(e)
                self.logger.error(
                    "Major issue with RedditPostSearch: " + str(e))
                print helpers.color(error, warning=True)
            try:
                RawHtml = dl.requesturl(url, useragent=self.UserAgent)
            except Exception as e:
                error = " [!] Fail during Request to Reddit (Check Connection):" + \
                    str(e)
                self.logger.error(
                    "Fail during Request to Reddit (Check Connection): " + str(e))
                print helpers.color(error, warning=True)
            self.Html += RawHtml
            # reddit seems to increment by 25 in cases
            self.Counter += 25

    def get_emails(self):
        Parse = Parser.Parser(self.Html)
        Parse.genericClean()
        Parse.urlClean()
        FinalOutput = Parse.GrepFindEmails()
        HtmlResults = Parse.BuildResults(FinalOutput, self.name)
        JsonResults = Parse.BuildJson(FinalOutput, self.name)
        self.logger.debug("RedditPostSearch completed search")
        return FinalOutput, HtmlResults, JsonResults
