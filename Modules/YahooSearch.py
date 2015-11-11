 #!/usr/bin/env python

# Class will have the following properties:
# 1) name / description
# 2) main name called "ClassName"
# 3) execute function (calls everthing it neeeds)
# 4) places the findings into a queue

# Adapted from theHarvester:
# https://github.com/laramies/theHarvester/blob/master/discovery/yahoosearch.py
# https://emailhunter.co

import configparser
import requests
import time
from Helpers import helpers
from Helpers import Parser


class ClassName:

    def __init__(self, Domain):
        self.name = "Yahoo Search for Emails"
        self.description = "Uses Yahoo to search for emails, parses them out of the Html"
        config = configparser.ConfigParser()
        try:
            config.read('Common/SimplyEmail.ini')
            self.Domain = Domain
            self.Quanity = int(config['YahooSearch']['StartQuantity'])
            self.UserAgent = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
            self.Limit = int(config['YahooSearch']['QueryLimit'])
            self.Counter = int(config['YahooSearch']['QueryStart'])
            self.Html = ""
        except:
            print helpers.color("[*] Major Settings for YahooSearch are missing, EXITING!\n", warning=True)

    def execute(self):
        self.search()
        FinalOutput, HtmlResults = self.get_emails()
        return FinalOutput, HtmlResults

    def search(self):
        while self.Counter <= self.Limit and self.Counter <= 1000:
            time.sleep(1)
            try:
                url = 'https://search.yahoo.com/search?p=' + str(self.Domain) + \
                    '&b=' + str(self.Counter) + "&pz=" + str(self.Quanity)
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
            self.Counter += 100

    def get_emails(self):
        Parse = Parser.Parser(self.Html)
        Parse.genericClean()
        Parse.urlClean()
        FinalOutput = Parse.GrepFindEmails()
        HtmlResults = Parse.BuildResults(FinalOutput,self.name)
        return FinalOutput, HtmlResults
