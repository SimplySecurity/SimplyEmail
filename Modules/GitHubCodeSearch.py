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

# This method will do the following:
# 1) Get raw HTML for lets say enron.com (https://github.com/search?utf8=✓&q=enron.com+&type=Code&ref=searchresults)
#    This is mainly do to the API not supporting code searched with out known repo or user :(
# 2) Use beautiful soup to parse the results of the first (5) pages for <A HREF> tags that start with "/"
# 3) Ueses a list of URL's and places that raw HTML into a on value
# 4) Sends to parser for results

# Here was a simple version of parsing a page:
# urlist = []
# FinalHtml = ""
# r = requests.get(
#     "https://github.com/search?utf8=%E2%9C%93&q=enron.com+&type=Code&ref=searchresults")
# html = r.content
# soup = BeautifulSoup(html)
# for a in soup.findAll('a', href=True):
#     a = a['href']
#     if a.startswith('/'):
#         time.sleep(1)
#         a = 'https://github.com' + str(a)
#         html = requests.get(a)
#         print "[!] Hitting: " + a
#         FinalHtml += html.content
# with open("temps.html", "w") as myfile:
#     output = myfile.write(FinalHtml)


class ClassName(object):

    def __init__(self, domain, verbose=False):
        self.apikey = False
        self.name = "Searching GitHub Code"
        self.description = "Search GitHub code for emails using a large pool of code searches"
        self.domain = domain
        config = configparser.ConfigParser()
        self.Html = ""
        self.verbose = verbose
        try:
            self.UserAgent = {
                'User-Agent': helpers.getua()}
            config.read('Common/SimplyEmail.ini')
            self.Depth = int(config['GitHubSearch']['PageDepth'])
            self.Counter = int(config['GitHubSearch']['QueryStart'])
        except:
            print helpers.color(" [*] Major Settings for GitHubSearch are missing, EXITING!\n", warning=True)

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
                p = ' [*] GitHub Code Search on page: ' + str(self.Counter)
                print helpers.color(p, firewall=True)
            try:
                url = "https://github.com/search?p=" + str(self.Counter) + "&q=" + \
                    str(self.domain) + "+&ref=searchresults&type=Code&utf8=✓"
                r = dl.requesturl(url, useragent=self.UserAgent, raw=True, timeout=10)
                if r.status_code != 200:
                    break
            except Exception as e:
                error = " [!] Major isself.Counter += 1sue with GitHub Search:" + \
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
                url = "https://github.com" + url
                html = dl.requesturl(url, useragent=self.UserAgent, timeout=10)
                self.Html += html
            except Exception as e:
                error = " [!] Connection Timed out on Github Search:" + str(e)
                print helpers.color(error, warning=True)

    def get_emails(self):
        Parse = Parser.Parser(self.Html)
        Parse.genericClean()
        Parse.urlClean()
        FinalOutput = Parse.GrepFindEmails()
        HtmlResults = Parse.BuildResults(FinalOutput, self.name)
        return FinalOutput, HtmlResults
