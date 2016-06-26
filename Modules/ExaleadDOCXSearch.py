# !/usr/bin/env python

# Class will have the following properties:
# 1) name / description
# 2) main name called "ClassName"
# 3) execute function (calls everything it needs)
# 4) places the findings into a queue
import configparser
import requests
import time
import logging
from Helpers import Converter
from Helpers import helpers
from Helpers import Parser
from Helpers import Download
from bs4 import BeautifulSoup

# import for "'ascii' codec can't decode byte" error
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
# import for "'ascii' codec can't decode byte" error


class ClassName(object):

    def __init__(self, Domain, verbose=False):
        self.apikey = False
        self.name = "Exalead DOCX Search for Emails"
        self.description = "Uses Exalead Dorking to search DOCXs for emails"
        config = configparser.ConfigParser()
        try:
            self.logger = logging.getLogger("SimplyEmail.ExaleadDOCXSearch")
            config.read('Common/SimplyEmail.ini')
            self.Domain = Domain
            self.Quanity = int(config['ExaleadDOCXSearch']['StartQuantity'])
            self.UserAgent = {
                'User-Agent': helpers.getua()}
            self.Limit = int(config['ExaleadDOCXSearch']['QueryLimit'])
            self.Counter = int(config['ExaleadDOCXSearch']['QueryStart'])
            self.verbose = verbose
            self.urlList = []
            self.Text = ""
        except Exception as e:
            self.logger.critical("ExaleadDOCXSearch module failed to __init__: " + str(e))
            p = " [*] Major Settings for ExaleadDOCXSearch are missing, EXITING: " + e
            print helpers.color(p, warning=True)

    def execute(self):
        self.logger.debug("ExaleadDOCXSearch module started")
        self.search()
        FinalOutput, HtmlResults, JsonResults = self.get_emails()
        return FinalOutput, HtmlResults, JsonResults

    def download_file(self, url):
        local_filename = url.split('/')[-1]
        # NOTE the stream=True parameter
        r = requests.get(url, stream=True)
        with open(local_filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=1024):
                if chunk:  # filter out keep-alive new chunks
                    f.write(chunk)
                    # f.flush() commented by recommendation from J.F.Sebastian
        return local_filename

    def search(self):
        convert = Converter.Converter(verbose=self.verbose)
        while self.Counter <= self.Limit:
            time.sleep(1)
            if self.verbose:
                p = ' [*] Exalead Search on page: ' + str(self.Counter)
                self.logger.info("ExaleadDOCXSearch on page: " + str(self.Counter))
                print helpers.color(p, firewall=True)
            try:
                url = 'http://www.exalead.com/search/web/results/?q="%40' + self.Domain + \
                      '"+filetype:docx&elements_per_page=' + \
                    str(self.Quanity) + '&start_index=' + str(self.Counter)
            except Exception as e:
                self.logger.error("Issue building URL to search")
                error = " [!] Major issue with Exalead DOCX Search: " + str(e)
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
                self.urlList = [h2.a["href"]
                                for h2 in soup.findAll('h4', class_='media-heading')]
            except Exception as e:
                self.logger.error("Fail during parsing result: " + str(e))
                error = " [!] Fail during parsing result: " + str(e)
                print helpers.color(error, warning=True)
            self.Counter += 30

        # now download the required files
        try:
            for url in self.urlList:
                if self.verbose:
                    p = ' [*] Exalead DOCX search downloading: ' + str(url)
                    self.logger.info("Starting download of DOCX: " + str(url))
                    print helpers.color(p, firewall=True)
                try:
                    filetype = ".docx"
                    dl = Download.Download(self.verbose)
                    FileName, FileDownload = dl.download_file(url, filetype)
                    if FileDownload:
                        if self.verbose:
                            self.logger.info("File was downloaded: " + str(url))
                            p = ' [*] Exalead DOCX file was downloaded: ' + \
                                str(url)
                            print helpers.color(p, firewall=True)
                        self.Text += convert.convert_docx_to_txt(FileName)
                except Exception as e:
                    self.logger.error("Issue with opening DOCX Files: " + str(e))
                    error = " [!] Issue with opening DOCX Files:%s\n" % (str(e))
                    print helpers.color(error, warning=True)
                try:
                    dl.delete_file(FileName)
                except Exception as e:
                    print e
        except Exception as e:
            p = " [*] No DOCX's to download from Exalead: " + e
            self.logger.info("No DOCX's to download from Exalead: " + str(e))
            print helpers.color(p, firewall=True)

        if self.verbose:

            p = ' [*] Searching DOCX from Exalead Complete'
            self.logger.info("Searching DOCX from Exalead Complete")
            print helpers.color(p, status=True)

    def get_emails(self):
        Parse = Parser.Parser(self.Text)
        Parse.genericClean()
        Parse.urlClean()
        FinalOutput = Parse.GrepFindEmails()
        HtmlResults = Parse.BuildResults(FinalOutput, self.name)
        JsonResults = Parse.BuildJson(FinalOutput, self.name)
        self.logger.debug('ExaleadDOCXSearch completed search')
        return FinalOutput, HtmlResults, JsonResults
