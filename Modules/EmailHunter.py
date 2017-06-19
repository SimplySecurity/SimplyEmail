#!/usr/bin/env python
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

# Searches for personal emails, ex. ajohnson@example.com vs. contact@example.com
# Personal emails more useful for phishing

# https://api.hunter.io/v2/domain-search?domain=any.com&type=personal&limit=100&api_key=your_api_key


class ClassName(object):

    def __init__(self, domain, verbose=False):
        self.apikey = True
        self.name = "EmailHunter API"
        self.description = "Search the EmailHunter DB for potential emails"
        self.domain = domain
        config = configparser.ConfigParser()
        self.results = []
        self.verbose = verbose
        try:
            self.logger = logging.getLogger("SimplyEmail.EmailHunter")
            config.read('Common/SimplyEmail.ini')
            self.UserAgent = str(config['GlobalSettings']['UserAgent'])
            self.apikeyv = str(config['APIKeys']['EmailHunter'])
        except Exception as e:
            self.logger.critical("EmailHunter module failed to __init__: " + str(e))
            print helpers.color(" [*] Major Settings for EmailHunter are missing, EXITING!\n", warning=True)

    def execute(self):
        self.logger.debug("EmailHunter module started")
        self.process()
        FinalOutput, HtmlResults, JsonResults = self.get_emails()
        return FinalOutput, HtmlResults, JsonResults

    def process(self):
        dl = Download.Download(self.verbose)
        try:
            # This returns a JSON object
            url = "https://api.hunter.io/v2/domain-search?domain=" + \
                self.domain + "&type=personal&limit=100&api_key=" + self.apikeyv
            r = dl.requesturl(url, useragent=self.UserAgent, raw=True)
        except Exception as e:
            error = "[!] Major issue with EmailHunter Search:" + str(e)
            print helpers.color(error, warning=True)
        try:
            results = r.json()
            # pprint(results)
            # Check to make sure we got data back from the API
            if int(results['meta']['results']) > 0:
                # The API starts at 0 for the first value
                x = 0
                EmailCount = int(results['meta']['results'])
                # We will itirate of the Json object for the index objects
                while x < EmailCount:
                    self.results.append(results['data']['emails'][int(x)]['value'])
                    x += 1
            else:
                error = ' [!] EmailHunter API returned no results'
        except Exception as e:
            pass
        if self.verbose:
            p = ' [*] EmailHunter completed JSON request'
            print helpers.color(p, firewall=True)

    def get_emails(self):
        # Make sure you remove any newlines
        Parse = Parser.Parser(self.results)
        FinalOutput = Parse.CleanListOutput()
        HtmlResults = Parse.BuildResults(FinalOutput, self.name)
        JsonResults = Parse.BuildJson(FinalOutput, self.name)
        self.logger.debug('EmailHunter completed search')
        return FinalOutput, HtmlResults, JsonResults
