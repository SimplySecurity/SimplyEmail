#!/usr/bin/env python

# Class will have the following properties:
# 1) name / description
# 2) main name called "ClassName"
# 3) execute function (calls everthing it neeeds)
# 4) places the findings into a queue
import configparser
import requests
import time
from Helpers import helpers
from Helpers import Parser


class ClassName(object):

    def __init__(self, Domain, verbose=False):
        self.apikey = False
        self.name = "RedditPost Search for Emails"
        self.description = "Uses RedditPosts to search for emails, and Parse the raw results ATM"
        config = configparser.ConfigParser()
        try:
            config.read('Common/SimplyEmail.ini')
            self.Domain = Domain
            self.UserAgent = {
                'User-Agent': helpers.getua()}
            self.Limit = int(config['RedditPostSearch']['QueryLimit'])
            self.Counter = int(config['RedditPostSearch']['QueryStart'])
            self.verbose = verbose
            self.Html = ""
        except:
            print helpers.color("[*] Major Settings for RedditPostSearch are missing, EXITING!\n", warning=True)

    def execute(self):
        self.search()
        FinalOutput, HtmlResults = self.get_emails()
        return FinalOutput, HtmlResults

    def search(self):
        while self.Counter <= self.Limit and self.Counter <= 1000:
            time.sleep(1)
            if self.verbose:
                p = '[*] RedditPost Search on result: ' + str(self.Counter)
                print helpers.color(p, firewall=True)
            try:
                url = "https://www.reddit.com/search?q=%40" + str(self.Domain) + \
                    "&restrict_sr=&sort=relevance&t=all&count=" + str(self.Counter) + \
                    '&after=t3_3mkrqg'
            except Exception as e:
                error = "[!] Major issue with RedditPost search:" + str(e)
                print helpers.color(error, warning=True)
            try:
                r = requests.get(url, headers=self.UserAgent)
            except Exception as e:
                error = "[!] Fail during Request to Reddit (Check Connection):" + \
                    str(e)
                print helpers.color(error, warning=True)
            results = r.content
            self.Html += results
            # reddit seems to increment by 25 in cases
            self.Counter += 25

    def get_emails(self):
        Parse = Parser.Parser(self.Html)
        Parse.genericClean()
        Parse.urlClean()
        FinalOutput = Parse.GrepFindEmails()
        HtmlResults = Parse.BuildResults(FinalOutput, self.name)
        return FinalOutput, HtmlResults
