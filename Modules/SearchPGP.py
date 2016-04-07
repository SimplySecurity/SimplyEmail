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


class ClassName(object):

    def __init__(self, domain, verbose=False):
        self.apikey = False
        self.name = "Searching PGP"
        self.description = "Search the PGP database for potential emails"
        self.domain = domain
        config = configparser.ConfigParser()
        self.results = ""
        try:
            config.read('Common/SimplyEmail.ini')
            self.server = str(config['SearchPGP']['KeyServer'])
            self.hostname = str(config['SearchPGP']['Hostname'])
            self.UserAgent = str(config['GlobalSettings']['UserAgent'])
            self.verbose = verbose
        except:
            print helpers.color("[*] Major Settings for SearchPGP are missing, EXITING!\n", warning=True)

    def execute(self):
        self.process()
        FinalOutput, HtmlResults = self.get_emails()
        return FinalOutput, HtmlResults

    def process(self):
        try:
            url = "http://pgp.rediris.es:11371/pks/lookup?search=" + \
                self.domain + "&op=index"
            r = requests.get(url)
        except Exception as e:
            error = "[!] Major issue with PGP Search:" + str(e)
            print helpers.color(error, warning=True)
        if self.verbose:
            p = '[*] Searching PGP Complete'
            print helpers.color(p, firewall=True)
        self.results = r.content

    def get_emails(self):
        Parse = Parser.Parser(self.results)
        FinalOutput = Parse.GrepFindEmails()
        HtmlResults = Parse.BuildResults(FinalOutput, self.name)
        return FinalOutput, HtmlResults
