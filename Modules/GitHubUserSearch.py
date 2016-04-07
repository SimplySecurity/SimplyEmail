#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
import configparser
import time
from Helpers import Parser
from Helpers import helpers

# https://github.com/search?p=1&q=gmail.com&ref=searchresults&type=Users&utf8=
# Main goal is to search for potential users
# on this you can eaily setoff abuse rate limiting
# so lets add a 5 sec sleep per request


class ClassName:

    def __init__(self, domain, verbose=False):
        self.apikey = False
        self.name = "Searching GitHubUser Search"
        self.description = "Search GitHubUser for emails the user search function"
        self.domain = domain
        config = configparser.ConfigParser()
        self.verbose = verbose
        self.Html = ""
        try:
            config.read('Common/SimplyEmail.ini')
            self.UserAgent = {
                'User-Agent': helpers.getua()}
            self.Depth = int(config['GitHubUserSearch']['PageDepth'])
            self.Counter = int(config['GitHubUserSearch']['QueryStart'])
        except:
            print helpers.color("[*] Major Settings for GitHubUserSearch are missing, EXITING!\n", warning=True)

    def execute(self):
        self.search()
        FinalOutput, HtmlResults = self.get_emails()
        return FinalOutput, HtmlResults

    def search(self):
        while self.Counter <= self.Depth and self.Counter <= 100:
            time.sleep(6)
            if self.verbose:
                p = '[*] GitHubUser Search on page: ' + str(self.Counter)
                print helpers.color(p, firewall=True)
            try:
                url = 'https://github.com/search?p=' + str(self.Counter) + '&q=' + \
                    str(self.domain) + 'ref=searchresults&type=Users&utf8='
            except Exception as e:
                error = "[!] Major issue with GitHubUser Search:" + str(e)
                print helpers.color(error, warning=True)
            try:
                r = requests.get(url, headers=self.UserAgent)
            except Exception as e:
                error = "[!] Fail during Request to GitHubUser (Check Connection):" + \
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
        HtmlResults = Parse.BuildResults(FinalOutput, self.name)
        return FinalOutput, HtmlResults
