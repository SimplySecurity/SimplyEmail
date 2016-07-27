#!/usr/bin/env python

# Class will have the following properties:
# 1) name / description
# 2) main name called "ClassName"
# 3) execute function (calls everything it needs)
# 4) places the findings into a queue
import configparser
import time
from Helpers import helpers
from Helpers import Parser
from Helpers import Download


class ClassName(object):

    def __init__(self, Domain, verbose=False):
        self.apikey = False
        self.name = "Google Search for Emails"
        self.description = "Uses Google to search for emails, parses them out of the"
        config = configparser.ConfigParser()
        try:
            config.read('Common/SimplyEmail.ini')
            self.Domain = Domain
            self.Quanity = int(config['GoogleSearch']['StartQuantity'])
            self.UserAgent = {
                'User-Agent': helpers.getua()}
            self.Limit = int(config['GoogleSearch']['QueryLimit'])
            self.Counter = int(config['GoogleSearch']['QueryStart'])
            self.Sleep = int(config['SleepConfig']['QuerySleep'])
            self.Jitter = int(config['SleepConfig']['QueryJitter'])
            self.verbose = verbose
            self.Html = ""
        except:
            print helpers.color(" [*] Major Settings for GoogleSearch are missing, EXITING!\n", warning=True)

    def execute(self):
        self.search()
        FinalOutput, HtmlResults, JsonResults = self.get_emails()
        return FinalOutput, HtmlResults, JsonResults

    def search(self):
        dl = Download.Download(self.verbose)
        while self.Counter <= self.Limit and self.Counter <= 1000:
            time.sleep(1)
            if self.verbose:
                p = ' [*] Google Search on page: ' + str(self.Counter)
                print helpers.color(p, firewall=True)
            try:
                url = "http://www.google.com/search?num=" + str(self.Quanity) + "&start=" + \
                    str(self.Counter) + "&hl=en&meta=&q=%40\"" + \
                    self.Domain + "\""
            except Exception as e:
                error = " [!] Major issue with Google Search:" + str(e)
                print helpers.color(error, warning=True)
            try:
                results = dl.requesturl(url, useragent=self.UserAgent)
            except Exception as e:
                error = " [!] Fail during Request to Google (Check Connection):" + \
                    str(e)
                print helpers.color(error, warning=True)
            try:
                # Url = r.url
                dl.GoogleCaptchaDetection(results)
            except Exception as e:
                print e
            self.Html += results
            self.Counter += 100
            helpers.modsleep(self.Sleep, jitter=self.Jitter)
    def get_emails(self):
        Parse = Parser.Parser(self.Html)
        Parse.genericClean()
        Parse.urlClean()
        FinalOutput = Parse.GrepFindEmails()
        HtmlResults = Parse.BuildResults(FinalOutput, self.name)
        JsonResults = Parse.BuildJson(FinalOutput, self.name)
        return FinalOutput, HtmlResults, JsonResults
