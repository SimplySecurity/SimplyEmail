#!/usr/bin/env python
import requests
import configparser
from Helpers import Parser
from Helpers import helpers

# Class will have the following properties:
# 1) name / description
# 2) main name called "ClassName"
# 3) execute function (calls everthing it neeeds)
# 4) places the findings into a queue

# https://whoisology.com/archive_11/microsoft.com


class ClassName:

    def __init__(self, domain, verbose=False):
        self.apikey = False
        self.name = "Searching Whoisology"
        self.description = "Search the Whoisology database for potential POC emails"
        self.domain = domain
        config = configparser.ConfigParser()
        self.results = ""
        try:
            config.read('Common/SimplyEmail.ini')
            self.UserAgent = str(config['GlobalSettings']['UserAgent'])
            self.verbose = verbose
        except:
            print helpers.color("[*] Major Settings for Search Whoisology are missing, EXITING!\n", warning=True)

    def execute(self):
        self.process()
        FinalOutput, HtmlResults = self.get_emails()
        return FinalOutput, HtmlResults

    def process(self):
        try:
            if self.verbose:
                p = '[*] Yahoo Whoisology request underway'
                print helpers.color(p, firewall=True)
            url = "https://whoisology.com/archive_11/" + \
                self.domain
            r = requests.get(url)
        except Exception as e:
            error = "[!] Major issue with Whoisology Search:" + str(e)
            print helpers.color(error, warning=True)
        self.results = r.content

    def get_emails(self):
        Parse = Parser.Parser(self.results)
        Parse.genericClean()
        Parse.urlClean()
        FinalOutput = Parse.GrepFindEmails()
        HtmlResults = Parse.BuildResults(FinalOutput, self.name)
        return FinalOutput, HtmlResults
