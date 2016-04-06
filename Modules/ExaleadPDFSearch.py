# !/usr/bin/env python

# Class will have the following properties:
# 1) name / description
# 2) main name called "ClassName"
# 3) execute function (calls everthing it neeeds)
# 4) places the findings into a queue
import configparser
import requests
import time
import re
import urlparse
import os
from Helpers import helpers
from Helpers import Parser
from Helpers import Download
from bs4 import BeautifulSoup
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from cStringIO import StringIO


class ClassName:
    def __init__(self, Domain, verbose=False):
        self.apikey = False
        self.name = "Exalead PDF Search for Emails"
        self.description = "Uses Exalead Dorking to search PDFs for emails"
        config = configparser.ConfigParser()
        try:
            config.read('Common/SimplyEmail.ini')
            self.Domain = Domain
            self.Quanity = int(config['ExaleadPDFSearch']['StartQuantity'])
            self.UserAgent = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
            self.Limit = int(config['ExaleadPDFSearch']['QueryLimit'])
            self.Counter = int(config['ExaleadPDFSearch']['QueryStart'])
            self.verbose = verbose
            self.urlList = []
            self.Text = ""
        except:
            print helpers.color(" [*] Major Settings for ExaleadPDFSearch are missing, EXITING!\n", warning=True)

    def convert_pdf_to_txt(self, path):
        rsrcmgr = PDFResourceManager()
        retstr = StringIO()
        codec = 'utf-8'
        laparams = LAParams()
        device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
        fp = file(path, 'rb')
        interpreter = PDFPageInterpreter(rsrcmgr, device)
        password = ""
        maxpages = 0
        caching = True
        pagenos = set()

        for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages, password=password, caching=caching,
                                      check_extractable=True):
            interpreter.process_page(page)

        text = retstr.getvalue()

        fp.close()
        device.close()
        retstr.close()
        return text

    def execute(self):
        self.search()
        FinalOutput, HtmlResults = self.get_emails()
        return FinalOutput, HtmlResults

    def search(self):
        while self.Counter <= self.Limit and self.Counter <= 10:
            time.sleep(1)
            if self.verbose:
                p = ' [*] Exalead Search on page: ' + str(self.Counter)
                print helpers.color(p, firewall=True)
            try:
                url = 'http://www.exalead.com/search/web/results/?q="%40' + self.Domain + \
                      '"+filetype:pdf&elements_per_page=' + str(self.Quanity) + '&start_index=' + str(self.Counter)
            except Exception as e:
                error = " [!] Major issue with Exalead PDF Search: " + str(e)
                print helpers.color(error, warning=True)
            try:
                r = requests.get(url, headers=self.UserAgent)
            except Exception as e:
                error = " [!] Fail during Request to Exalead (Check Connection):" + str(e)
                print helpers.color(error, warning=True)
            try:
                RawHtml = r.content
                self.Text += RawHtml  # sometimes url is broken but exalead search results contain e-mail
                soup = BeautifulSoup(RawHtml, "lxml")
                self.urlList = [h2.a["href"] for h2 in soup.findAll('h4', class_='media-heading')]
            except Exception as e:
                error = " [!] Fail during parsing result: " + str(e)
                print helpers.color(error, warning=True)
            self.Counter += 30

        # now download the required files
        try:
            for url in self.urlList:
                if self.verbose:
                    p = ' [*] Exalead PDF search downloading: ' + str(url)
                    print helpers.color(p, firewall=True)
                try:
                    filetype = ".pdf"
                    dl = Download.Download(self.verbose)
                    FileName, FileDownload = dl.download_file(url, filetype)
                    if FileDownload:
                        if self.verbose:
                            p = ' [*] Exalead PDF file was downloaded: ' + str(url)
                            print helpers.color(p, firewall=True)
                        self.Text += self.convert_pdf_to_txt(FileName)
                except Exception as e:
                    pass
                try:
                    dl.delete_file(FileName)
                except Exception as e:
                    print e
        except:
            print helpers.color(" [*] No PDF's to download from Exalead!\n", firewall=True)

        if self.verbose:
            p = ' [*] Searching PDF from Exalead Complete'
            print helpers.color(p, status=True)

    def get_emails(self):
        Parse = Parser.Parser(self.Text)
        Parse.genericClean()
        Parse.urlClean()
        FinalOutput = Parse.GrepFindEmails()
        HtmlResults = Parse.BuildResults(FinalOutput, self.name)
        return FinalOutput, HtmlResults
