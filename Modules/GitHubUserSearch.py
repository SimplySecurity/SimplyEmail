#!/usr/bin/env python
# -*- coding: utf-8 -*-
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
            print helpers.color(" [*] Major Settings for GitHubUserSearch are missing, EXITING!\n", warning=True)

    def execute(self):
        self.search()
        FinalOutput, HtmlResults, JsonResults = self.get_emails()
        return FinalOutput, HtmlResults, JsonResults

    def search(self):
        dl = Download.Download(verbose=self.verbose)
        while self.Counter <= self.Depth and self.Counter <= 100:
            helpers.modsleep(5)
            if self.verbose:
                p = ' [*] GitHubUser Search on page: ' + str(self.Counter)
                print helpers.color(p, firewall=True)
            try:
                url = 'https://github.com/search?p=' + str(self.Counter) + '&q=' + \
                    str(self.domain) + 'ref=searchresults&type=Users&utf8='
            except Exception as e:
                error = " [!] Major issue with GitHubUser Search:" + str(e)
                print helpers.color(error, warning=True)
            try:
                r = dl.requesturl(
                    url, useragent=self.UserAgent, raw=True, timeout=10)
            except Exception as e:
                error = " [!] Fail during Request to GitHubUser (Check Connection):" + \
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
        JsonResults = Parse.BuildJson(FinalOutput, self.name)
        return FinalOutput, HtmlResults, JsonResults
