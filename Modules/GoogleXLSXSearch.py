#!/usr/bin/env python

# Class will have the following properties:
# 1) name / description
# 2) main name called "ClassName"
# 3) execute function (calls everything it needs)
# 4) places the findings into a queue
import requests
import urlparse
import configparser
import time
import logging
from Helpers import Download
from Helpers import helpers
from Helpers import Parser
from Helpers import Converter
from BeautifulSoup import BeautifulSoup


class ClassName(object):

    def __init__(self, Domain, verbose=False):
        self.apikey = False
        self.name = "Google XLSX Search for Emails"
        self.description = "Uses Google Dorking to search for emails"
        config = configparser.ConfigParser()
        try:
            self.logger = logging.getLogger("SimplyEmail.GoogleXlsxSearch")
            config.read('Common/SimplyEmail.ini')
            self.Domain = Domain
            self.Quanity = int(config['GoogleXlsxSearch']['StartQuantity'])
            self.Limit = int(config['GoogleXlsxSearch']['QueryLimit'])
            self.UserAgent = {
                'User-Agent': helpers.getua()}
            self.Counter = int(config['GoogleXlsxSearch']['QueryStart'])
            self.verbose = verbose
            self.urlList = []
            self.Text = ""
        except Exception as e:
            self.logger.critical(
                'GoogleXlsxSearch module failed to load: ' + str(e))
            print helpers.color(" [*] Major Settings for GoogleXlsxSearch are missing, EXITING!\n", warning=True)

    def execute(self):
        self.logger.debug("GoogleXlsxSearch Started")
        self.search()
        FinalOutput, HtmlResults = self.get_emails()
        return FinalOutput, HtmlResults

    def search(self):
        convert = Converter.Converter(verbose=self.verbose)
        while self.Counter <= self.Limit and self.Counter <= 100:
            time.sleep(1)
            if self.verbose:
                p = ' [*] Google XLSX Search on page: ' + str(self.Counter)
                self.logger.info(
                    "Google XLSX Search on page: " + str(self.Counter))
                print helpers.color(p, firewall=True)
            try:
                urly = "https://www.google.com/search?q=site:" + \
                    self.Domain + "+filetype:xlsx&start=" + str(self.Counter)
            except Exception as e:
                error = " [!] Major issue with Google XLSX Search:" + str(e)
                self.logger.error(
                    "GoogleXlsxSearch failed to build url: " + str(e))
                print helpers.color(error, warning=True)
            try:
                r = requests.get(urly)
            except Exception as e:
                error = " [!] Fail during Request to Google (Check Connection):" + \
                    str(e)
                self.logger.error(
                    "GoogleXlsxSearch failed to request url (Check Connection): " + str(e))
                print helpers.color(error, warning=True)
            RawHtml = r.content
            soup = BeautifulSoup(RawHtml)
            # I use this to parse my results, for URLS to follow
            for a in soup.findAll('a'):
                try:
                    # https://stackoverflow.com/questions/21934004/not-getting-proper-links-
                    # from-google-search-results-using-mechanize-and-beautifu/22155412#22155412?
                    # newreg=01f0ed80771f4dfaa269b15268b3f9a9
                    l = urlparse.parse_qs(
                        urlparse.urlparse(a['href']).query)['q'][0]
                    if l.startswith('http') or l.startswith('www'):
                        if "webcache.googleusercontent.com" not in l:
                            self.urlList.append(l)
                except:
                    pass
            self.Counter += 10
        # now download the required files
        self.logger.debug(
            "GoogleXlsxSearch completed HTML result query, starting downloads")
        try:
            for url in self.urlList:
                if self.verbose:
                    p = ' [*] Google XLSX search downloading: ' + str(url)
                    self.logger.info(
                        "Google XLSX search downloading: " + str(url))
                    print helpers.color(p, firewall=True)
                try:
                    filetype = ".xlsx"
                    dl = Download.Download(self.verbose)
                    FileName, FileDownload = dl.download_file(url, filetype)
                    if FileDownload:
                        if self.verbose:
                            p = ' [*] Google XLSX file was downloaded: ' + \
                                str(url)
                            self.logger.info(
                                "Google XLSX file was downloaded: " + str(url))
                            print helpers.color(p, firewall=True)
                        self.Text += convert.convert_Xlsx_to_Csv(FileName)
                    # print self.Text
                except Exception as e:
                    print helpers.color(" [!] Issue with opening Xlsx Files\n", firewall=True)
                    self.logger.error("Google XLSX had issue opening file")
                try:
                    dl.delete_file(FileName)
                except Exception as e:
                    self.logger.error(
                        "Google XLSX failed to delete file: " + str(e))
        except Exception as e:
            print helpers.color(" [*] No XLSX's to download from google!\n", firewall=True)
            self.logger.error("No XLSX's to download from google! " + str(e))

    def get_emails(self):
        Parse = Parser.Parser(self.Text)
        Parse.genericClean()
        Parse.urlClean()
        FinalOutput = Parse.GrepFindEmails()
        HtmlResults = Parse.BuildResults(FinalOutput, self.name)
        self.logger.debug('GoogleXlsxSearch completed search')
        return FinalOutput, HtmlResults
