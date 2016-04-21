#!/usr/bin/env python
# -*- coding: utf-8 -*-
import configparser
from BeautifulSoup import BeautifulSoup
from Helpers import Download
from Helpers import Parser
from Helpers import helpers

# Class will have the following properties:
# 1) name / description
# 2) main name called "ClassName"
# 3) execute function (calls everything it needs)
# 4) places the findings into a queue


# https://gist.github.com/search?utf8=✓&q=%40enron.com&ref=searchresults

class ClassName(object):

    def __init__(self, domain, verbose=False):
        self.apikey = False
        self.name = "Searching GitHubGist Code"
        self.description = "Search GitHubGist code for emails using a large pool of code searches"
        self.domain = domain
        config = configparser.ConfigParser()
        self.Html = ""
        self.verbose = verbose
        try:
            self.UserAgent = {
                'User-Agent': helpers.getua()}
            config.read('Common/SimplyEmail.ini')
            self.Depth = int(config['GitHubGistSearch']['PageDepth'])
            self.Counter = int(config['GitHubGistSearch']['QueryStart'])
        except:
            print helpers.color(" [*] Major Settings for GitHubGistSearch are missing, EXITING!\n", warning=True)

    def execute(self):
        self.process()
        FinalOutput, HtmlResults = self.get_emails()
        return FinalOutput, HtmlResults

    def process(self):
        dl = Download.Download(verbose=self.verbose)
        # Get all the USER code Repos
        # https://github.com/search?p=2&q=enron.com+&ref=searchresults&type=Code&utf8=✓
        UrlList = []
        while self.Counter <= self.Depth:
            if self.verbose:
                p = ' [*] GitHub Gist Search Search on page: ' + \
                    str(self.Counter)
                print helpers.color(p, firewall=True)
            try:
                # search?p=2&q=%40enron.com&ref=searchresults&utf8=✓
                url = "https://gist.github.com/search?p=" + str(self.Counter) + "&q=%40" + \
                    str(self.domain) + "+&ref=searchresults&utf8=✓"
                r = dl.requesturl(url, useragent=self.UserAgent, raw=True, timeout=10)
                if r.status_code != 200:
                    break
            except Exception as e:
                error = " [!] Major issue with GitHubGist Search:" + \
                    str(e)
                print helpers.color(error, warning=True)
            RawHtml = r.content
            # Parse the results for our URLS)
            soup = BeautifulSoup(RawHtml)
            for a in soup.findAll('a', href=True):
                a = a['href']
                if a.startswith('/'):
                    UrlList.append(a)
            self.Counter += 1
        # Now take all gathered URL's and gather the HTML content needed
        for url in UrlList:
            try:
                url = "https://gist.github.com" + url
                html = dl.requesturl(url, useragent=self.UserAgent, timeout=10)
                self.Html += html
            except Exception as e:
                error = " [!] Connection Timed out on GithubGist Search:" + \
                    str(e)
                print helpers.color(error, warning=True)

    def get_emails(self):
        Parse = Parser.Parser(self.Html)
        Parse.genericClean()
        Parse.urlClean()
        FinalOutput = Parse.GrepFindEmails()
        HtmlResults = Parse.BuildResults(FinalOutput, self.name)
        return FinalOutput, HtmlResults
