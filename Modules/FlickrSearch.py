#!/usr/bin/env python
import configparser
from Helpers import Download
from Helpers import Parser
from Helpers import helpers

# Class will have the following properties:
# 1) name / description
# 2) main name called "ClassName"
# 3) execute function (calls everything it needs)
# 4) places the findings into a queue


class ClassName(object):

    def __init__(self, domain, verbose=False):
        self.apikey = False
        self.name = "Searching Flickr"
        self.description = "Search the Flickr top relvant results for emails"
        self.domain = domain
        config = configparser.ConfigParser()
        self.results = ""
        self.verbose = verbose
        try:
            self.UserAgent = {
                'User-Agent': helpers.getua()}
            config.read('Common/SimplyEmail.ini')
            self.HostName = str(config['FlickrSearch']['Hostname'])
        except:
            print helpers.color(" [*] Major Settings for FlickrSearch are missing, EXITING!\n", warning=True)

    def execute(self):
        self.process()
        FinalOutput, HtmlResults, JsonResults = self.get_emails()
        return FinalOutput, HtmlResults, JsonResults

    def process(self):
        dl = Download.Download(verbose=self.verbose)
        try:
            url = "https://www.flickr.com/search/?text=%40" + self.domain
            rawhtml = dl.requesturl(url, useragent=self.UserAgent)
        except Exception as e:
            error = " [!] Major issue with Flickr Search:" + str(e)
            print helpers.color(error, warning=True)
        self.results += rawhtml
        if self.verbose:
            p = ' [*] FlickrSearch has completed'
            print helpers.color(p, firewall=True)
        # https://www.flickr.com/search/?text=%40microsoft.com
        # is an example of a complete request for "@microsoft.com"

    def get_emails(self):
        Parse = Parser.Parser(self.results)
        FinalOutput = Parse.GrepFindEmails()
        HtmlResults = Parse.BuildResults(FinalOutput, self.name)
        JsonResults = Parse.BuildJson(FinalOutput, self.name)
        return FinalOutput, HtmlResults, JsonResults
