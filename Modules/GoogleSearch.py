#!/usr/bin/env python

# Class will have the following properties:
# 1) name / description
# 2) main name called "ClassName"
# 3) execute function (calls everthing it neeeds)
# 4) places the findings into a queue
import configparser
import requests
import time
from Helpers import helpers
from Helpers import Parser


class ClassName:

    def __init__(self, Domain):
        self.name = "Google Search for Emails"
        self.description = "Uses google to search for emails, parses them out of the"
        config = configparser.ConfigParser()
        try:
            config.read('Common/SimplyEmail.ini')
            self.Domain = Domain
            self.Quanity = int(config['GoogleSearch']['StartQuantity'])
            self.UserAgent = str(config['GlobalSettings']['UserAgent'])
            self.Limit = int(config['GoogleSearch']['QueryLimit'])
            self.Counter = int(config['GoogleSearch']['QueryStart'])
            self.Html = ""
        except:
            print helpers.color("[*] Major Settings for GoogleSearch are missing, EXITING!\n", warning=True)

    def execute(self):
        self.search()
        FinalOutput = self.get_emails()
        return FinalOutput

    def search(self):
        while self.Counter <= self.Limit and self.Counter <= 1000:
            time.sleep(1)
            try:
                url = "http://www.google.com/search?num=" + str(self.Quanity) + \
                    "&start=" + str(self.Counter) + \
                    "&hl=en&meta=&q=%40\"" + self.Domain + "\""
            except Exception as e:
                error = "[!] Major issue with Google Search:" + str(e)
                print helpers.color(error, warning=True)
            try:
                r = requests.get(url)
            except Exception as e:
                error = "[!] Fail during Request to Google (Check Connection):" + \
                    str(e)
                print helpers.color(error, warning=True)
            results = r.content
            self.Html += results
            self.Counter += 100

    def get_emails(self):
        Parse = Parser.Parser(self.Html)
        FinalOutput = Parse.GrepFindEmails()
        return FinalOutput
