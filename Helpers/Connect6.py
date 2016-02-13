#!/usr/bin/env python
import helpers
import requests
import configparser
import urllib
import urlparse
from BeautifulSoup import BeautifulSoup



class Connect6Scraper:
    '''
    A simple class to scrape names from connect6.com
    '''
    def __init__(self, domain, Verbose=False):
      config = configparser.ConfigParser()
      try:
        config.read('Common/SimplyEmail.ini')
        self.UserAgent = {
          'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
        self.domain = domain
        self.FinalAnswer = ''
        self.verbose = Verbose
      except Exception as e:
        print e

    '''
    Try to find the connect6 url for the domain
    you are trageting.
    '''
    def Connect6AutoUrl(self):
      # Using startpage to attempt to get the URL
      # https://www.google.com/search?q=site:connect6.com+domain.com
      try:
        # This returns a JSON object
        urllist = []
        url = "https://www.google.com/search?q=site:connect6.com+%22" + self.domain + '%22'
        r = requests.get(url, headers=self.UserAgent)
      except Exception as e:
        error = "[!] Major issue with Google Search: for Connect6 URL" + str(e)
        print helpers.color(error, warning=True)
      try:
        RawHtml = r.content
        soup = BeautifulSoup(RawHtml)
        for a in soup.findAll('a', href=True):
          try:
            l = urlparse.parse_qs(urlparse.urlparse(a['href']).query)['q']
            if 'site:connect6.com' not in l[0]:
              l = l[0].split(":")
              urllist.append(l[2])
          except:
            pass
        return urllist
      except Exception as e:
        print e
    '''
    Downloads raw source of Connects6 page.
    '''
    def Connect6Download(self, url):
      NameList = []
      try:
        if url.startswith('http') or url.startswith('https'):
          r = requests.get(url, headers=self.UserAgent)
        else:
          url = 'http://' + str(url)
          r = requests.get(url, headers=self.UserAgent)
      except Exception as e:
        error = " [!] Major issue with Downloading Connect6 source:" + str(e)
        print helpers.color(error, warning=True)
      try:
        if r:
          RawHtml = r.content
          soup = BeautifulSoup(RawHtml)
          try:
            for utag in soup.findAll("ul", { "class" : "directoryList" }):
              for litag in utag.findAll('li'):
                NameList.append(litag.text)
          except:
            pass
          return NameList
        #for a in soup.findAll('a', href=True):
      except Exception as e:
        print e

    def Connect6ParseName(self, raw):
      '''
      Takes a raw non parsed name from connect 6.
      Returns a list of the Name [first, last]
      '''
      # Adapted by:
      #   Author: @Harmj0y
      #   Author Blog: http://t.co/ZYPKvkeayX
      #   helper to try to parse all the types of naming convent
      try:
        if raw.strip() != "":
            if "(" in raw:
                raw = raw.split("(")[0]

            if "," in raw:
                raw = raw.split(",")[0]

            if "/" in raw:
                raw = raw.split("/")[0]

            raw = raw.strip()

            if raw.endswith("."):
                return None

            if len(raw) == 1:
                return None

            if "LinkedIn" in raw:
                return None

            if "\"" in raw:
                return None

            parts = raw.split()

            firstName = ""
            lastName = ""

            if len(parts) > 2:
                if "(" in parts[1]:
                    # assume nickname in middle
                    firstName = parts[0].strip()
                    lastName = parts[2].strip()
                elif len(parts[2]) < 4:
                    # assume certification
                    firstName = parts[0].strip()
                    lastName = parts[1].strip()
                else:
                    # assume FIRST MIDDLE LASTNAME
                    firstName = parts[0].strip()
                    lastName = parts[2].strip()

            elif len(parts) == 2:
                # assume FIRST LASTNAME
                firstName = parts[0].strip()
                lastName = parts[1].strip()

            if "." in lastName:
                return None

            if len(lastName) < 2:
                return None

            if "\"" in lastName:
                lastName = lastName.replace("\"", "")

            if "'" in lastName:
                lastName = lastName.replace("'", "")

            else:
                return [firstName, lastName]
      except Exception as e:
        e = ' [!] Failed to parse name: ' + str(e)



