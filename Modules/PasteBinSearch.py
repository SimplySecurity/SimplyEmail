# !/usr/bin/env python

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
from bs4 import BeautifulSoup

class ClassName:

    def __init__(self, Domain, verbose=False):
        self.name = "PasteBin Search for Emails"
        self.description = "Uses pastebin to search for emails, parses them out of the"
        config = configparser.ConfigParser()
        try:
            config.read('Common/SimplyEmail.ini')
            self.Domain = Domain
            self.Quanity = int(config['GooglePasteBinSearch']['StartQuantity'])
            self.UserAgent = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
            self.Limit = int(config['GooglePasteBinSearch']['QueryLimit'])
            self.Counter = int(config['GooglePasteBinSearch']['QueryStart'])
            self.verbose = verbose
            self.urlList = []
            self.Text = ""
        except:
            print helpers.color("[*] Major Settings for PasteBinSearch are missing, EXITING!\n", warning=True)

    def execute(self):
        self.search()
        FinalOutput, HtmlResults = self.get_emails()
        return FinalOutput, HtmlResults


    def search(self):
        while self.Counter <= self.Limit and self.Counter <= 100:
            time.sleep(1)
            if self.verbose:
                p = '[*] Google Search for PasteBin on page: ' + str(self.Counter)
                print helpers.color(p, firewall=True)
            try:
                url = "http://www.google.com/search?num=" + str(self.Quanity) + "&start=" + str(self.Counter) + \
                      '&hl=en&meta=&q=site:pastebin.com+"%40' + self.Domain + '"'
            except Exception as e:
                error = "[!] Major issue with Google Search for PasteBin:" + str(e)
                print helpers.color(error, warning=True)

            try:
                r = requests.get(url, headers=self.UserAgent)
            except Exception as e:
                error = "[!] Fail during Request to PasteBin (Check Connection):" + str(e)
                print helpers.color(error, warning=True)
            try:
                RawHtml = r.content
                soup = BeautifulSoup(RawHtml)
                for a in soup.select('.r a'):
                    if "/u/" not in str(a['href']): # remove urls like pastebin.com/u/Anonymous
                        self.urlList.append(a['href'])
            except Exception as e:
                error = "[!] Fail during parsing result: " + str(e)
                print helpers.color(error, warning=True)
            self.Counter += 100
        # Now take all gathered URL's and gather the Raw content needed
        for Url in self.urlList:
            try:
                Url = "http://pastebin.com/raw/" + str(Url).split('/')[3]
                data = requests.get(Url, timeout=2)
                self.Text += data.content
            except Exception as e:
                error = "[!] Connection Timed out on PasteBin Search:" + str(e)
                print helpers.color(error, warning=True)

        if self.verbose:
            p = '[*] Searching PasteBin Complete'
            print helpers.color(p, firewall=True)

    def get_emails(self):
        Parse = Parser.Parser(self.Text)
        Parse.genericClean()
        Parse.urlClean()
        FinalOutput = Parse.GrepFindEmails()
        HtmlResults = Parse.BuildResults(FinalOutput, self.name)
        return FinalOutput, HtmlResults
