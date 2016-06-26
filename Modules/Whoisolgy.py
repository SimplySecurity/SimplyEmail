#!/usr/bin/env python
import requests
import configparser
import logging
from Helpers import Parser
from Helpers import helpers

# Class will have the following properties:
# 1) name / description
# 2) main name called "ClassName"
# 3) execute function (calls everything it needs)
# 4) places the findings into a queue

# https://whoisology.com/archive_11/microsoft.com


class ClassName(object):

    def __init__(self, domain, verbose=False):
        self.apikey = False
        self.name = "Searching Whoisology"
        self.logger = logging.getLogger("SimplyEmail.Whoisology")
        self.description = "Search the Whoisology database for potential POC emails"
        self.domain = domain
        config = configparser.ConfigParser()
        self.results = ""
        try:
            config.read('Common/SimplyEmail.ini')
            self.UserAgent = {
                'User-Agent': helpers.getua()}
            self.verbose = verbose
        except Exception as e:
            self.logger.critical(
                'Whoisology module failed to __init__: ' + str(e))
            print helpers.color("[*] Major Settings for Search Whoisology are missing, EXITING!\n", warning=True)

    def execute(self):
        self.logger.debug("Whoisology Started")
        self.process()
        FinalOutput, HtmlResults, JsonResults = self.get_emails()
        return FinalOutput, HtmlResults, JsonResults

    def process(self):
        try:
            if self.verbose:
                self.logger.info("Whoisology request started")
                p = ' [*] Whoisology request started'
                print helpers.color(p, firewall=True)
            url = "https://whoisology.com/archive_11/" + \
                self.domain
            r = requests.get(url)
        except Exception as e:
            error = "[!] Major issue with Whoisology Search:" + str(e)
            self.logger.error("Whoisology can download source (Check Connection)")
            print helpers.color(error, warning=True)
        self.results = r.content

    def get_emails(self):
        Parse = Parser.Parser(self.results)
        Parse.genericClean()
        Parse.urlClean()
        FinalOutput = Parse.GrepFindEmails()
        HtmlResults = Parse.BuildResults(FinalOutput, self.name)
        JsonResults = Parse.BuildJson(FinalOutput, self.name)
        self.logger.debug('Whoisology completed search')
        return FinalOutput, HtmlResults, JsonResults
