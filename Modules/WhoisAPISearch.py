# http://api.hackertarget.com/whois/?q=verisgroup.com
# !/usr/bin/env python

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
        self.name = "Searching Whois"
        self.description = "Search the Whois database for potential POC emails"
        self.domain = domain
        config = configparser.ConfigParser()
        self.verbose = verbose
        self.results = ""
        try:
            self.logger = logging.getLogger("SimplyEmail.WhoisAPISearch")
            config.read('Common/SimplyEmail.ini')
            self.UserAgent = str(config['GlobalSettings']['UserAgent'])
        except Exception as e:
            self.logger.critical(
                'WhoisAPISearch module failed to __init__: ' + str(e))
            print helpers.color(" [*] Major Settings for Search Whois are missing, EXITING!\n", warning=True)

    def execute(self):
        self.logger.debug("WhoisAPISearch Started")
        self.process()
        FinalOutput, HtmlResults, JsonResults = self.get_emails()
        return FinalOutput, HtmlResults, JsonResults

    def process(self):
        try:
            if self.verbose:
                p = ' [*] Requesting API on HackerTarget whois'
                self.logger.info("Requesting API on HackerTarget whois")
                print helpers.color(p, firewall=True)
            url = "http://api.hackertarget.com/whois/?q=" + \
                self.domain
            r = requests.get(url)
        except Exception as e:
            error = " [!] Major issue with Whois Search:" + str(e)
            self.logger.error(
                "Failed to request URL (Check Connection): " + str(e))
            print helpers.color(error, warning=True)
        self.results = r.content

    def get_emails(self):
        Parse = Parser.Parser(self.results)
        FinalOutput = Parse.GrepFindEmails()
        HtmlResults = Parse.BuildResults(FinalOutput, self.name)
        JsonResults = Parse.BuildJson(FinalOutput, self.name)
        self.logger.debug('WhoisAPISearch completed search')
        return FinalOutput, HtmlResults, JsonResults
