 #!/usr/bin/env python

# Class will have the following properties:
# 1) name / description
# 2) main name called "ClassName"
# 3) execute function (calls everthing it neeeds)
# 4) places the findings into a queue
import re
import requests
import urlparse
import os
import configparser
import requests
import time
from Helpers import Download
from subprocess import Popen, PIPE
from Helpers import helpers
from Helpers import Parser
from BeautifulSoup import BeautifulSoup
from cStringIO import StringIO

class ClassName:

    def __init__(self, Domain, verbose=False):
        self.apikey = False
        self.name = "Google XLSX Search for Emails"
        self.description = "Uses Google Dorking to search for emails"
        config = configparser.ConfigParser()
        try:
            config.read('Common/SimplyEmail.ini')
            self.Domain = Domain
            self.Quanity = int(config['GoogleXlsxSearch']['StartQuantity'])
            self.UserAgent = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
            self.Limit = int(config['GoogleXlsxSearch']['QueryLimit'])
            self.Counter = int(config['GoogleXlsxSearch']['QueryStart'])
            self.verbose = verbose
            self.urlList = []
            self.Text = ""
        except:
            print helpers.color("[*] Major Settings for GoogleXlsxSearch are missing, EXITING!\n", warning=True)

    def execute(self):
        self.search()
        FinalOutput, HtmlResults = self.get_emails()
        return FinalOutput, HtmlResults


    def convert_Xlsx_to_Csv(self, path):
        # Using the Xlsx2csv tool seemed easy and was in python anyhow
        # it also supported custom delim :)
        cmd = ['xlsx2csv', path]
        p = Popen(cmd, stdout=PIPE)
        stdout, stderr = p.communicate()
        return stdout.decode('ascii', 'ignore')


    def search(self):
        while self.Counter <= self.Limit and self.Counter <= 100:
            time.sleep(1)
            if self.verbose:
                p = '[*] Google XLSX Search on page: ' + str(self.Counter)
                print helpers.color(p, firewall=True)
            try:
                urly = "https://www.google.com/search?q=site:" + self.Domain + "+filetype:xlsx&start=" + str(self.Counter)
            except Exception as e:
                error = "[!] Major issue with Google Search:" + str(e)
                print helpers.color(error, warning=True)
            try:
                r = requests.get(urly)
            except Exception as e:
                error = "[!] Fail during Request to Google (Check Connection):" + \
                    str(e)
                print helpers.color(error, warning=True)
            RawHtml = r.content
            soup = BeautifulSoup(RawHtml)
            # I use this to parse my results, for URLS to follow
            for a in soup.findAll('a'):
                  try:
                    # https://stackoverflow.com/questions/21934004/not-getting-proper-links-
                    # from-google-search-results-using-mechanize-and-beautifu/22155412#22155412?
                    # newreg=01f0ed80771f4dfaa269b15268b3f9a9
                    l = urlparse.parse_qs(urlparse.urlparse(a['href']).query)['q'][0]
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
                    p = '[*] Google XLSX search downloading: ' + str(url)
                    print helpers.color(p, firewall=True)
                try:
                    filetype = ".xlsx"
                    dl = Download.Download(self.verbose)
                    FileName, FileDownload = dl.download_file(url, filetype)
                    if FileDownload:
                        if self.verbose:
                            p = '[*] Google PDF file was downloaded: ' + str(url)
                            print helpers.color(p, firewall=True)
                        self.Text += self.convert_Xlsx_to_Csv(FileName)
                    # print self.Text
                except Exception as e:
                    print helpers.color("[!] Issue with opening Xlsx Files\n", firewall=True)
                try:
                    dl.delete_file(FileName)
                except Exception as e:
                    print e
        except:
            print helpers.color("[*] No XLSX's to download from google!\n", firewall=True)


    def get_emails(self):
        Parse = Parser.Parser(self.Text)
        Parse.genericClean()
        Parse.urlClean()
        FinalOutput = Parse.GrepFindEmails()
        HtmlResults = Parse.BuildResults(FinalOutput,self.name)
        return FinalOutput, HtmlResults
