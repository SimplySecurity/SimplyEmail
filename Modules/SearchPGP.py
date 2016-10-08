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


class ClassName(object):

    def __init__(self, domain, verbose=False):
        self.apikey = False
        self.name = "Searching PGP"
        self.description = "Search the PGP database for potential emails"
        self.domain = domain
        config = configparser.ConfigParser()
        self.results = ""
        try:
            self.logger = logging.getLogger("SimplyEmail.SearchPGP")
            config.read('Common/SimplyEmail.ini')
            self.server = str(config['SearchPGP']['KeyServer'])
            self.hostname = str(config['SearchPGP']['Hostname'])
            self.UserAgent = str(config['GlobalSettings']['UserAgent'])
            self.verbose = verbose
        except Exception as e:
            self.logger.critical(
                'SearchPGP module failed to __init__: ' + str(e))
            print helpers.color("[*] Major Settings for SearchPGP are missing, EXITING!\n", warning=True)

    def execute(self):
        self.logger.debug("SearchPGP started")
        self.process()
        FinalOutput, HtmlResults, JsonResults = self.get_emails()
        return FinalOutput, HtmlResults, JsonResults

    def process(self):
        try:
            url = "http://pgp.mit.edu/pks/lookup?search=" + \
                self.domain + "&op=index"
            self.logger.info("Requesting PGP keys")
            r = requests.get(url)
        except Exception as e:
            error = " [!] Major issue with PGP Search:" + str(e)
            self.logger.error("Major issue with PGP search: " + str(e))
            print helpers.color(error, warning=True)
        if self.verbose:
            p = ' [*] Searching PGP Complete'
            self.logger.info("SearchPGP Completed search")
            print helpers.color(p, firewall=True)
        self.results = r.content

    def get_emails(self):
        Parse = Parser.Parser(self.results)
        FinalOutput = Parse.GrepFindEmails()
        HtmlResults = Parse.BuildResults(FinalOutput, self.name)
        JsonResults = Parse.BuildJson(FinalOutput, self.name)
        self.logger.debug("SearchPGP completed search")
        return FinalOutput, HtmlResults, JsonResults
