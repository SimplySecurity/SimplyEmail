#!/usr/bin/env python
# Port from theHarvester! Shout out to him for the code:
# https://github.com/laramies/theHarvester/blob/master/discovery/asksearch.py
import configparser
import requests
from Helpers import Parser
from Helpers import helpers

# Class will have the following properties:
# 1) name / description
# 2) main name called "ClassName"
# 3) execute function (calls everthing it neeeds)
# 4) places the findings into a queue


class ClassName:

    def __init__(self, Domain, verbose=False):
        self.name = "Ask Search for Emails"
        self.description = "Simple Ask Search for Emails"
        config = configparser.ConfigParser()
        try:
            config.read('Common/SimplyEmail.ini')
            self.UserAgent = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
            self.PageLimit = int(config['AskSearch']['QueryPageLimit'])
            self.Counter = int(config['AskSearch']['QueryStart'])
            self.Domain = Domain
            self.verbose = verbose
            self.Html = ""
        except:
            print helpers.color("[*] Major Settings for Ask Search are missing, EXITING!\n", warning=True)

    def execute(self):
        self.process()
        FinalOutput, HtmlResults = self.get_emails()
        return FinalOutput, HtmlResults

    def process(self):
        while self.Counter <= self.PageLimit:
            if self.verbose:
                p = '[*] AskSearch on page: ' + str(self.Counter)
                print helpers.color(p, firewall=True)
            try:
                url = 'http://www.ask.com/web?q=@' + str(self.Domain) + \
                    '&pu=10&page=' + str(self.Counter)
            except Exception as e:
                error = "[!] Major issue with Yahoo Search:" + str(e)
                print helpers.color(error, warning=True)
            try:
                r = requests.get(url, headers=self.UserAgent)
            except Exception as e:
                error = "[!] Fail during Request to Yahoo (Check Connection):" + \
                    str(e)
                print helpers.color(error, warning=True)
            results = r.content
            self.Html += results
            self.Counter += 1

    def get_emails(self):
        Parse = Parser.Parser(self.Html)
        Parse.genericClean()
        Parse.urlClean()
        FinalOutput = Parse.GrepFindEmails()
        HtmlResults = Parse.BuildResults(FinalOutput,self.name)
        return FinalOutput, HtmlResults
