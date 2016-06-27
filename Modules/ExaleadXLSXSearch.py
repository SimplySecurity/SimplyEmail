# !/usr/bin/env python

# Class will have the following properties:
# 1) name / description
# 2) main name called "ClassName"
# 3) execute function (calls everything it needs)
# 4) places the findings into a queue
import requests
import configparser
import time
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
        self.name = "Exalead XLSX Search for Emails"
        self.description = "Uses Exalead Dorking to search XLSXs for emails"
        config = configparser.ConfigParser()
        try:
            config.read('Common/SimplyEmail.ini')
            self.Domain = Domain
            self.Quanity = int(config['ExaleadXLSXSearch']['StartQuantity'])
            self.UserAgent = {
                'User-Agent': helpers.getua()}
            self.Limit = int(config['ExaleadXLSXSearch']['QueryLimit'])
            self.Counter = int(config['ExaleadXLSXSearch']['QueryStart'])
            self.verbose = verbose
            self.urlList = []
            self.Text = ""
        except:
            print helpers.color(" [*] Major Settings for ExaleadXLSXSearch are missing, EXITING!\n", warning=True)

    def execute(self):
        self.search()
        FinalOutput, HtmlResults, JsonResults = self.get_emails()
        return FinalOutput, HtmlResults, JsonResults

    def search(self):
        dl = Download.Download(verbose=self.verbose)
        convert = Converter.Converter(verbose=self.verbose)
        while self.Counter <= self.Limit:
            time.sleep(1)
            if self.verbose:
                p = ' [*] Exalead XLSX Search on page: ' + str(self.Counter)
                print helpers.color(p, firewall=True)
            try:
                url = 'http://www.exalead.com/search/web/results/?q="%40' + self.Domain + \
                      '"+filetype:xlsx&elements_per_page=' + \
                    str(self.Quanity) + '&start_index=' + str(self.Counter)
            except Exception as e:
                error = " [!] Major issue with Exalead XLSX Search:" + str(e)
                print helpers.color(error, warning=True)
            try:
                r = requests.get(url, headers=self.UserAgent)
            except Exception as e:
                error = " [!] Fail during Request to Exalead (Check Connection):" + str(
                    e)
                print helpers.color(error, warning=True)
            try:
                RawHtml = r.content
                # sometimes url is broken but exalead search results contain
                # e-mail
                self.Text += RawHtml
                soup = BeautifulSoup(RawHtml, "lxml")
                self.urlList = [h4.a["href"]
                                for h4 in soup.findAll('h4', class_='media-heading')]
            except Exception as e:
                error = " [!] Fail during parsing result: " + str(e)
                print helpers.color(error, warning=True)
            self.Counter += 30

        # now download the required files
        try:
            for url in self.urlList:
                if self.verbose:
                    p = ' [*] Exalead XLSX search downloading: ' + str(url)
                    print helpers.color(p, firewall=True)
                try:
                    filetype = ".xlsx"
                    FileName, FileDownload = dl.download_file(url, filetype)
                    if FileDownload:
                        if self.verbose:
                            p = ' [*] Exalead XLSX file was downloaded: ' + \
                                str(url)
                            print helpers.color(p, firewall=True)
                        self.Text += convert.convert_Xlsx_to_Csv(FileName)
                except Exception as e:
                    error = " [!] Issue with opening Xlsx Files:%s\n" % (str(e))
                    print helpers.color(error, warning=True)
                try:
                    dl.delete_file(FileName)
                except Exception as e:
                    print e
        except:
            print helpers.color("[*] No XLSX's to download from Exalead!\n", firewall=True)

        if self.verbose:
            p = ' [*] Searching XLSX from Exalead Complete'
            print helpers.color(p, status=True)

    def get_emails(self):
        Parse = Parser.Parser(self.Text)
        Parse.genericClean()
        Parse.urlClean()
        FinalOutput = Parse.GrepFindEmails()
        HtmlResults = Parse.BuildResults(FinalOutput, self.name)
        JsonResults = Parse.BuildJson(FinalOutput, self.name)
        return FinalOutput, HtmlResults, JsonResults
