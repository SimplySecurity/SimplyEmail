#!/usr/bin/env python
import requests
import configparser
from pprint import pprint
from Helpers import Parser
from Helpers import helpers

# Class will have the following properties:
# 1) name / description
# 2) main name called "ClassName"
# 3) execute function (calls everthing it neeeds)
# 4) places the findings into a queue

# https://emailhunter.co/trial/v1/search?offset=0&domain=any.com&format=json

class ClassName:

    def __init__(self, domain):
        self.name = "EmailHunter Trial API"
        self.description = "Search the EmailHunter DB for potential emails"
        self.domain = domain
        config = configparser.ConfigParser()
        self.results = []
        try:
            config.read('Common/SimplyEmail.ini')
            self.UserAgent = str(config['GlobalSettings']['UserAgent'])
        except:
            print helpers.color("[*] Major Settings for EmailHunter are missing, EXITING!\n", warning=True)

    def execute(self):
        self.process()
        FinalOutput, HtmlResults = self.get_emails()
        return FinalOutput, HtmlResults

    def process(self):
        try:
            # This returns a JSON object
            url = "https://emailhunter.co/trial/v1/search?offset=0&domain=" + \
                self.domain + "&format=json"
            r = requests.get(url)
        except Exception as e:
            error = "[!] Major issue with PGP Search:" + str(e)
            print helpers.color(error, warning=True)
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

    def get_emails(self):
        # Make sure you remove any newlines
        Parse = Parser.Parser(self.results)
        FinalOutput = Parse.CleanListOutput()
        HtmlResults = Parse.BuildResults(FinalOutput,self.name)
        return FinalOutput, HtmlResults