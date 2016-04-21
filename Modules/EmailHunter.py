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

# https://emailhunter.co/trial/v1/search?offset=0&domain=any.com&format=json


class ClassName(object):

    def __init__(self, domain, verbose=False):
        self.apikey = False
        self.name = "EmailHunter Trial API"
        self.description = "Search the EmailHunter DB for potential emails"
        self.domain = domain
        config = configparser.ConfigParser()
        self.results = []
        self.verbose = verbose
        try:
            self.logger = logging.getLogger("SimplyEmail.EmailHunter")
            config.read('Common/SimplyEmail.ini')
            self.UserAgent = str(config['GlobalSettings']['UserAgent'])
        except Exception as e:
            self.logger.critical("EmailHunter module failed to __init__: " + str(e))
            print helpers.color(" [*] Major Settings for EmailHunter are missing, EXITING!\n", warning=True)

    def execute(self):
        self.logger.debug("EmailHunter module started")
        self.process()
        FinalOutput, HtmlResults = self.get_emails()
        return FinalOutput, HtmlResults

    def process(self):
        dl = Download.Download(self.verbose)
        try:
            # This returns a JSON object
            url = "https://emailhunter.co/trial/v1/search?offset=0&domain=" + \
                self.domain + "&format=json"
            r = dl.requesturl(url, useragent=self.UserAgent, raw=True)
        except Exception as e:
            error = "[!] Major issue with EmailHunter Search:" + str(e)
            print helpers.color(error, warning=True)
        try:
            results = r.json()
            # pprint(results)
            # Check to make sure we got data back from the API
            if results['status'] == "success":
                # The API starts at 0 for the first value
                x = 0
                EmailCount = int(results['results'])
                # We will itirate of the Json object for the index objects
                while x < EmailCount:
                    self.results.append(results['emails'][int(x)]['value'])
                    x += 1
            if results['status'] == "error":
                # The API starts at 0 for the first value
                error = ' [!] EmailHunter Trial API failed: ' + \
                    str(results['message'])
                self.logger.error('EmailHunter Trial API failed: ' + str(results['message']))
                print helpers.color(error, firewall=True)
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
        self.logger.debug('EmailHunter completed search')
        return FinalOutput, HtmlResults
