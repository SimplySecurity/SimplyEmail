#!/usr/bin/env python
# Port from theHarvester! Shout out to him for the code:
# https://github.com/laramies/theHarvester/blob/master/discovery/asksearch.py
import configparser
import logging
from Helpers import Download
from Helpers import Parser
from Helpers import helpers

# Class will have the following properties:
# 1) name / description
# 2) main name called "ClassName"
# 3) execute function (calls everything it needs)
# 4) places the findings into a queue


class ClassName(object):

    def __init__(self, Domain, verbose=False):
        self.apikey = False
        self.logger = logging.getLogger("SimplyEmail.AskSearch")
        self.name = "Ask Search for Emails"
        self.description = "Simple Ask Search for Emails"
        config = configparser.ConfigParser()
        try:
            config.read('Common/SimplyEmail.ini')
            self.UserAgent = {
                'User-Agent': helpers.getua()}
            self.PageLimit = int(config['AskSearch']['QueryPageLimit'])
            self.Counter = int(config['AskSearch']['QueryStart'])
            self.Sleep = int(config['SleepConfig']['QuerySleep'])
            self.Jitter = int(config['SleepConfig']['QueryJitter'])
            self.Domain = Domain
            self.verbose = verbose
            self.Html = ""
        except Exception as e:
            self.logger.critical(
                'AskSearch module failed to load: ' + str(e))
            print helpers.color("[*] Major Settings for Ask Search are missing, EXITING!\n", warning=True)

    def execute(self):
        self.logger.debug("AskSearch module started")
        self.process()
        FinalOutput, HtmlResults, JsonResults = self.get_emails()
        return FinalOutput, HtmlResults, JsonResults

    def process(self):
        dl = Download.Download(self.verbose)
        while self.Counter <= self.PageLimit:
            if self.verbose:
                p = ' [*] AskSearch on page: ' + str(self.Counter)
                print helpers.color(p, firewall=True)
                self.logger.info('AskSearch on page: ' + str(self.Counter))
            try:
                url = 'http://www.ask.com/web?q=@' + str(self.Domain) + \
                    '&pu=10&page=' + str(self.Counter)
            except Exception as e:
                error = " [!] Major issue with Ask Search:" + str(e)
                self.logger.error('Major issue with Ask Search: ' + str(e))
                print helpers.color(error, warning=True)
            try:
                rawhtml = dl.requesturl(url, useragent=self.UserAgent)
            except Exception as e:
                error = " [!] Fail during Request to Ask (Check Connection):" + \
                    str(e)
                self.logger.error(
                    'Fail during Request to Ask (Check Connection): ' + str(e))
                print helpers.color(error, warning=True)
            self.Html += rawhtml
            self.Counter += 1
            helpers.modsleep(self.Sleep, jitter=self.Jitter)


    def get_emails(self):
        parse = Parser.Parser(self.Html)
        FinalOutput, HtmlResults = parse.extendedclean(self.name)
        JsonResults = parse.BuildJson(FinalOutput, self.name)
        self.logger.debug('AskSearch completed search')
        return FinalOutput, HtmlResults, JsonResults
