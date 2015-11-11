#!/usr/bin/env python

import requests
import configparser
import os
from Helpers import *


# Class will have the following properties:
# 1) name / description
# 2) main name called "ClassName"
# 3) execute function (calls everthing it neeeds)
# 4) places the findings into a queue

# http://www.oninstagram.com/profile/search?query=@gmail.com
# this allows raw query, even major like @gmail

class ClassName:

    def __init__(self, Domain):
        self.name = "OnionStagram Search For Instagram Users"
        self.description = "Uses OnionStagrams search engine"
        config = configparser.ConfigParser()
        try:
            config.read('Common/SimplyEmail.ini')
            self.Domain = Domain
            self.Html = ""
        except:
            print helpers.color("[*] Major Settings for OnionStagram are missing, EXITING!\n", warning=True)

    def execute(self):
        self.process()
        FinalOutput, HtmlResults = self.get_emails()
        return FinalOutput, HtmlResults

    def process(self):
        try:
        	# page seems to dynamicaly expand :)
            url = "http://www.oninstagram.com/profile/search?query=" + \
                self.Domain
            r = requests.get(url)
        except Exception as e:
            error = "[!] Major issue with OnionStagram Search:" + str(e)
            print helpers.color(error, warning=True)
        self.Html = r.content

    def get_emails(self):
        Parse = Parser.Parser(self.Html)
        Parse.genericClean()
        Parse.urlClean()
        FinalOutput = Parse.GrepFindEmails()
        HtmlResults = Parse.BuildResults(FinalOutput,self.name)
        return FinalOutput, HtmlResults
