#!/usr/bin/env python
import requests
import configparser
from Helpers import Parser
from Helpers import helpers

# Example POST request to use StartPage
# POST https://startpage.com/do/search

# Host: startpage.com
# User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:43.0) Gecko/20100101 Firefox/43.0
# Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
# Accept-Language: en-US,en;q=0.5
# Accept-Encoding: gzip, deflate
# Referer: https://www.startpage.com/do/search
# Connection: keep-alive

# Content-Type: application/x-www-form-urlencoded
# Content-Length: 147

# cmd=process_search&language=english&enginecount=1&pl=&abp=-1&hmb=1&hmb=1&ff=&theme=&flag_ac=0&cat=web&ycc=0&nj=0&query=%22%40verisgroup.com%22&pg=0

# So Send this:
# https://startpage.com/do/search?cmd=process_search&language=english&enginecount=1&pl=&abp=-1&hmb=1&hmb=1&ff=&theme=&flag_ac=0&cat=web&ycc=0&nj=0&query=%22%40verisgroup.com%22&pg=0

# NOTE they only display 9 results per page 

class ClassName:

    def __init__(self, domain):
        self.name = "Searching StartPage"
        self.description = "Search StartPages Custom google search engine(this will help when google is being google"
        self.domain = domain
        config = configparser.ConfigParser()
        self.Html = ""
        try:
            config.read('Common/SimplyEmail.ini')

            self.Quanity = int(config['StartPageSearch']['StartQuantity'])
            self.UserAgent = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
            self.Limit = int(config['StartPageSearch']['QueryLimit'])
            self.Counter = int(config['StartPageSearch']['QueryStart'])
        except:
            print helpers.color("[*] Major Settings for StartPage Settings are missing, EXITING!\n", warning=True)

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
                r = requests.get(url, headers=self.UserAgent)
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

