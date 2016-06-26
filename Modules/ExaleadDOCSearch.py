# !/usr/bin/env python

# Class will have the following properties:
# 1) name / description
# 2) main name called "ClassName"
# 3) execute function (calls everything it needs)
# 4) places the findings into a queue

import configparser
import logging
from Helpers import Download
from Helpers import helpers
from Helpers import Parser
from Helpers import Converter
from bs4 import BeautifulSoup

# import for "'ascii' codec can't decode byte" error
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
# import for "'ascii' codec can't decode byte" error


class ClassName(object):

    def __init__(self, Domain, verbose=False):
        self.apikey = False
        self.name = "Exalead DOC Search for Emails"
        self.description = "Uses Exalead Dorking to search DOCs for emails"
        config = configparser.ConfigParser()
        try:
            self.logger = logging.getLogger("SimplyEmail.ExaleadDOCSearch")
            config.read('Common/SimplyEmail.ini')
            self.Domain = Domain
            self.Quanity = int(config['ExaleadDOCSearch']['StartQuantity'])
            self.UserAgent = {
                'User-Agent': helpers.getua()}
            self.Limit = int(config['ExaleadDOCSearch']['QueryLimit'])
            self.Counter = int(config['ExaleadDOCSearch']['QueryStart'])
            self.verbose = verbose
            self.urlList = []
            self.Text = ""
        except Exception as e:
            self.logger.critical("ExaleadDOCSearch module failed to __init__: " + str(e))
            print helpers.color(" [*] Major Settings for Exalead are missing, EXITING!\n", warning=True)

    def execute(self):
        self.logger.debug("ExaleadDOCSearch module started")
        self.search()
        FinalOutput, HtmlResults, JsonResults = self.get_emails()
        return FinalOutput, HtmlResults, JsonResults

    def search(self):
        dl = Download.Download(self.verbose)
        convert = Converter.Converter(verbose=self.verbose)
        while self.Counter <= self.Limit and self.Counter <= 10:
            helpers.modsleep(1)
            if self.verbose:
                p = ' [*] Exalead DOC Search on page: ' + str(self.Counter)
                self.logger.info('ExaleadDOCSearch on page: ' + str(self.Counter))
                print helpers.color(p, firewall=True)
            try:
                url = 'http://www.exalead.com/search/web/results/?q="%40' + self.Domain + \
                      '"+filetype:word&elements_per_page=' + \
                    str(self.Quanity) + '&start_index=' + str(self.Counter)
            except Exception as e:
                self.logger.error('ExaleadDOCSearch could not build URL')
                error = " [!] Major issue with Exalead DOC Search: " + str(e)
                print helpers.color(error, warning=True)
            try:
                RawHtml = dl.requesturl(url, useragent=self.UserAgent)
                # sometimes url is broken but exalead search results contain
                # e-mail
                self.Text += RawHtml
                soup = BeautifulSoup(RawHtml, "lxml")
                self.urlList = [h2.a["href"]
                                for h2 in soup.findAll('h4', class_='media-heading')]
            except Exception as e:
                self.logger.error('ExaleadDOCSearch could not request / parse HTML')
                error = " [!] Fail during parsing result: " + str(e)
                print helpers.color(error, warning=True)
            self.Counter += 30

        # now download the required files
        try:
            for url in self.urlList:
                if self.verbose:
                    p = ' [*] Exalead DOC search downloading: ' + str(url)
                    self.logger.info('ExaleadDOCSearch downloading: ' + str(url))
                    print helpers.color(p, firewall=True)
                try:
                    filetype = ".doc"
                    dl = Download.Download(self.verbose)
                    FileName, FileDownload = dl.download_file(url, filetype)
                    if FileDownload:
                        if self.verbose:
                            p = ' [*] Exalead DOC file was downloaded: ' + \
                                str(url)
                            self.logger.info('ExaleadDOCSearch downloaded: ' + str(p))
                            print helpers.color(p, firewall=True)
                        ft = helpers.filetype(FileName).lower()
                        if 'word' in ft:
                            self.Text += convert.convert_doc_to_txt(FileName)
                        else:
                            self.logger.warning('Downloaded file is not a DOC: ' + ft)
                except Exception as e:
                    error = " [!] Issue with opening DOC Files:%s\n" % (str(e))
                    print helpers.color(error, warning=True)
                try:
                    dl.delete_file(FileName)
                except Exception as e:
                    print e
        except Exception as e:
            self.logger.error("ExaleadDOCSearch no doc's to download")
            print helpers.color(" [*] No DOC's to download from Exalead!\n", firewall=True)

        if self.verbose:
            p = ' [*] Searching DOC from Exalead Complete'
            print helpers.color(p, status=True)

    def get_emails(self):
        Parse = Parser.Parser(self.Text)
        Parse.genericClean()
        Parse.urlClean()
        FinalOutput = Parse.GrepFindEmails()
        HtmlResults = Parse.BuildResults(FinalOutput, self.name)
        JsonResults = Parse.BuildJson(FinalOutput, self.name)
        self.logger.debug('ExaleadDOCSearch completed search')
        return FinalOutput, HtmlResults, JsonResults
