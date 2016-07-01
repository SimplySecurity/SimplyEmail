#!/usr/bin/env python

# Class will have the following properties:
# 1) name / description
# 2) main name called "ClassName"
# 3) execute function (calls everything it needs)
# 4) places the findings into a queue

# Adapted from theHarvester:
# https://github.com/laramies/theHarvester/blob/master/discovery/yahoosearch.py
# https://emailhunter.co

import configparser
import requests
import time
import logging
from Helpers import helpers
from Helpers import Parser


class ClassName(object):

    def __init__(self, Domain, verbose=False):
        self.apikey = False
        self.name = "Yahoo Search for Emails"
        self.description = "Uses Yahoo to search for emails, parses them out of the Html"
        config = configparser.ConfigParser()
        try:
            config.read('Common/SimplyEmail.ini')
            self.logger = logging.getLogger("SimplyEmail.YahooSearch")
            self.Domain = Domain
            self.Quanity = int(config['YahooSearch']['StartQuantity'])
            self.UserAgent = {
                'User-Agent': helpers.getua()}
            self.Limit = int(config['YahooSearch']['QueryLimit'])
            self.Counter = int(config['YahooSearch']['QueryStart'])
            self.Sleep = int(config['SleepConfig']['QuerySleep'])
            self.Jitter = int(config['SleepConfig']['QueryJitter'])
            self.verbose = verbose
            self.Html = ""
        except Exception as e:
            self.logger.critical(
                'YahooSearch module failed to load: ' + str(e))
            print helpers.color(" [*] Major Settings for YahooSearch are missing, EXITING!\n", warning=True)

    def execute(self):
        self.logger.debug("AskSearch Started")
        self.search()
        FinalOutput, HtmlResults, JsonResults = self.get_emails()
        return FinalOutput, HtmlResults, JsonResults

    def search(self):
        while self.Counter <= self.Limit and self.Counter <= 1000:
            time.sleep(1)
            if self.verbose:
                p = ' [*] Yahoo Search on page: ' + str(self.Counter)
                self.logger.info("YahooSearch on page:" + str(self.Counter))
                print helpers.color(p, firewall=True)
            try:
                url = 'https://search.yahoo.com/search?p=' + str(self.Domain) + \
                    '&b=' + str(self.Counter) + "&pz=" + str(self.Quanity)
            except Exception as e:
                error = " [!] Major issue with Yahoo Search:" + str(e)
                self.logger.error("Yahoo Search can not create URL:")
                print helpers.color(error, warning=True)
            try:
                self.logger.debug("YahooSearch starting request on: " + str(url))
                r = requests.get(url, headers=self.UserAgent)
            except Exception as e:
                error = " [!] Fail during Request to Yahoo (Check Connection):" + \
                    str(e)
                self.logger.error("YahooSearch failed to request (Check Connection)")
                print helpers.color(error, warning=True)
            results = r.content
            self.Html += results
            self.Counter += 100
            #helpers.modsleep(self.Sleep, jitter=self.Jitter)

    def get_emails(self):
        Parse = Parser.Parser(self.Html)
        Parse.genericClean()
        Parse.urlClean()
        FinalOutput = Parse.GrepFindEmails()
        HtmlResults = Parse.BuildResults(FinalOutput, self.name)
        JsonResults = Parse.BuildJson(FinalOutput, self.name)
        self.logger.debug('YahooSearch completed search')
        return FinalOutput, HtmlResults, JsonResults