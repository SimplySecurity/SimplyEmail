#!/usr/bin/env python
import string
import requests
import configparser
from Helpers import Parser
from Helpers import helpers

# Class will have the following properties:
# 1) name / description
# 2) main name called "ClassName"
# 3) execute function (calls everthing it neeeds)
# 4) places the findings into a queue


class ClassName:

    def __init__(self, domain):
        self.name = "Searching Flicker"
        self.description = "Search the Flicker top relvant results for emails"
        self.domain = domain
        config = configparser.ConfigParser()
        self.results = ""
        try:
            config.read('Common/SimplyEmail.ini')
            self.HostName = str(config['FlickrSearch']['Hostname'])
            self.UserAgent = str(config['GlobalSettings']['UserAgent'])
        except:
            print helpers.color("[*] Major Settings for FlickrSearch are missing, EXITING!\n", warning=True)

    def execute(self):
        self.process()
        FinalOutput = self.get_emails()
        return FinalOutput

    def process(self):
        try:
            url = "https://www.flickr.com/search/?text=%40" + self.domain
            r = requests.get(url)
        except Exception as e:
            error = "[!] Major issue with Flickr Search:" + str(e)
            print helpers.color(error, warning=True)
        self.results = r.content
        # https://www.flickr.com/search/?text=%40microsoft.com
        # is an example of a complete request for "@microsoft.com"

    def get_emails(self):
        Parse = Parser.Parser(self.results)
        FinalOutput = Parse.GrepFindEmails()
        return FinalOutput
