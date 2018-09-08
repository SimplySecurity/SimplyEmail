#!/usr/bin/env python

import configparser
import logging
import subprocess
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
        self.name = "ARIN WHOIS Search"
        self.description = "Search the ARIN WHOIS database for potential emails"
        self.domain = domain
        config = configparser.ConfigParser()
        self.verbose = verbose
        self.results = ""
        try:
            self.logger = logging.getLogger("SimplyEmail.WhoisScrape")
            config.read('Common/SimplyEmail.ini')
        except Exception as e:
            self.logger.critical(
                'WhoisScrape module failed to __init__: ' + str(e))
            print helpers.color(" [*] Major Settings for WhoisScrape are missing, EXITING!\n", warning=True)

    def execute(self):
        self.logger.debug("WhoisScrape Started")
        self.process()
        FinalOutput, HtmlResults, JsonResults = self.get_emails()
        return FinalOutput, HtmlResults, JsonResults

    def process(self):
        try:
            if self.verbose:
                p = ' [*] Requesting whois data from whois.arin.net'
                self.logger.info("Requesting whois data from whois.arin.net")
                print helpers.color(p, firewall=True)
            r = subprocess.check_output(["whois", "-h", "whois.arin.net", "e @ " + self.domain])
        except Exception as e:
            error = " [!] Major issue with ARIN WHOIS Search:" + str(e)
            self.logger.error(
                "Failed to execute whois: " + str(e))
            print helpers.color(error, warning=True)
        self.results = r

    def get_emails(self):
        Parse = Parser.Parser(self.results)
        FinalOutput = Parse.GrepFindEmails()
        HtmlResults = Parse.BuildResults(FinalOutput, self.name)
        JsonResults = Parse.BuildJson(FinalOutput, self.name)
        self.logger.debug('WhoisScrape completed search')
        return FinalOutput, HtmlResults, JsonResults
