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
from Helpers import Download
from Helpers import Converter
from Helpers import helpers
from Helpers import Parser
from BeautifulSoup import BeautifulSoup


class ClassName(object):

    def __init__(self, Domain, verbose=False):
        self.apikey = False
        self.name = "Google DOC Search for Emails"
        self.description = "Uses Google Dorking to search for emails"
        config = configparser.ConfigParser()
        try:
            config.read('Common/SimplyEmail.ini')
            self.Domain = Domain
            self.Quanity = int(config['GoogleDocSearch']['StartQuantity'])
            self.UserAgent = {
                'User-Agent': helpers.getua()}
            self.Limit = int(config['GoogleDocSearch']['QueryLimit'])
            self.Counter = int(config['GoogleDocSearch']['QueryStart'])
            self.verbose = verbose
            self.urlList = []
            self.Text = ""
        except:
            print helpers.color("[*] Major Settings for GoogleDocSearch are missing, EXITING!\n", warning=True)

    def execute(self):
        self.search()
        FinalOutput, HtmlResults = self.get_emails()
        return FinalOutput, HtmlResults

    def search(self):
        dl = Download.Download(self.verbose)
        convert = Converter.Converter(verbose=self.verbose)
        while self.Counter <= self.Limit and self.Counter <= 100:
            time.sleep(1)
            if self.verbose:
                p = ' [*] Google DOC Search on page: ' + str(self.Counter)
                print helpers.color(p, firewall=True)
            try:
                urly = "https://www.google.com/search?q=site:" + \
                    self.Domain + "+filetype:doc&start=" + str(self.Counter)
            except Exception as e:
                error = " [!] Major issue with Google Search:" + str(e)
                print helpers.color(error, warning=True)
            try:
                r = requests.get(urly)
            except Exception as e:
                error = " [!] Fail during Request to Google (Check Connection):" + \
                    str(e)
                print helpers.color(error, warning=True)
            RawHtml = r.content
            # check for captcha
            try:
                # Url = r.url
                dl.GoogleCaptchaDetection(RawHtml)
            except Exception as e:
                print e
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
        try:
            for url in self.urlList:
                if self.verbose:
                    p = ' [*] Google DOC search downloading: ' + str(url)
                    print helpers.color(p, firewall=True)
                try:
                    filetype = ".doc"
                    FileName, FileDownload = dl.download_file(url, filetype)
                    if FileDownload:
                        if self.verbose:
                            p = ' [*] Google DOC file was downloaded: ' + \
                                str(url)
                            print helpers.color(p, firewall=True)
                        self.Text += convert.convert_doc_to_txt(FileName)
                    # print self.Text
                except Exception as e:
                    print helpers.color(" [!] Issue with opening Doc Files\n", firewall=True)
                try:
                    dl.delete_file(FileName)
                except Exception as e:
                    print e
        except:
            print helpers.color(" [*] No DOC's to download from Google!\n", firewall=True)

    def get_emails(self):
        Parse = Parser.Parser(self.Text)
        Parse.genericClean()
        Parse.urlClean()
        FinalOutput = Parse.GrepFindEmails()
        HtmlResults = Parse.BuildResults(FinalOutput, self.name)
        return FinalOutput, HtmlResults
