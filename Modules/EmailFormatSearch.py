#!/usr/bin/env python
import logging
from Helpers import Download
from Helpers import Parser
from Helpers import helpers

# Class will have the following properties:
# 1) name / description
# 2) main name called "ClassName"
# 3) execute function (calls everything it needs)
# 4) places the findings into a queue

class ClassName(object):

    def __init__(self, Domain, verbose=False):
        self.apikey = False
        self.logger = logging.getLogger("SimplyEmail.EmailFormatSearch")
        self.name = "EmailFormat Search for Emails"
        self.description = "Simple EmailFormat Search for Emails"
        self.UserAgent = {'User-Agent': helpers.getua()}
        self.Domain = Domain
        self.verbose = verbose
        self.Html = ""

    def execute(self):
        self.logger.debug("EmailFormatSearch module started")
        self.process()
        FinalOutput, HtmlResults, JsonResults = self.get_emails()
        return FinalOutput, HtmlResults, JsonResults

    def process(self):
        dl = Download.Download(self.verbose)
        try:
            url = 'https://www.email-format.com/d/' + str(self.Domain)
        except Exception as e:
            error = " [!] Major issue with EmailFormat Search:" + str(e)
            self.logger.error('Major issue with EmailFormat Search: ' + str(e))
            print helpers.color(error, warning=True)
        try:
            rawhtml = dl.requesturl(url, useragent=self.UserAgent)                                          
        except Exception as e:
            error = " [!] Fail during request to EmailFormat (Check Connection):" + \
                str(e)
            self.logger.error(
                'Fail during request to EmailFormat (Check Connection): ' + str(e))
            print helpers.color(error, warning=True)
        self.Html += rawhtml

    def get_emails(self):
        parse = Parser.Parser(self.Html)
        FinalOutput, HtmlResults = parse.extendedclean(self.name)
        JsonResults = parse.BuildJson(FinalOutput, self.name)
        self.logger.debug('EmailFormatSearch completed search')
        return FinalOutput, HtmlResults, JsonResults
