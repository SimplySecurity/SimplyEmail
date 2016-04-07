#!/usr/bin/env python
import helpers
import configparser
import mechanize
from bs4 import BeautifulSoup


# This class has been adapted from (@pan0pt1c0n):
# https://github.com/pan0pt1c0n/PhishBait/blob/master/Bing_Scraper.py

class LinkedinScraper(object):

    '''
    A simple class to scrape names from bing.com for
    LinkedIn names.
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

    def LinkedInNames(self):
        # This function simply uses
        # Bing to scrape for names and
        # returns a list of list names.
        try:
            br = mechanize.Browser()
            br.set_handle_robots(False)
            self.domain = self.domain.split('.')
            self.domain = self.domain[0]
            r = br.open('http://www.bing.com/search?q=(site%3A%22www.linkedin.com%2Fin%2F%22%20OR%20site%3A%22www.linkedin.com%2Fpub%2F%22)%20%26%26%20(NOT%20site%3A%22www.linkedin.com%2Fpub%2Fdir%2F%22)%20%26%26%20%22' +
                        self.domain + '%22&qs=n&form=QBRE&pq=(site%3A%22www.linkedin.com%2Fin%2F%22%20or%20site%3A%22www.linkedin.com%2Fpub%2F%22)%20%26%26%20(not%20site%3A%22www.linkedin.com%2Fpub%2Fdir%2F%22)%20%26%26%20%22'+self.domain+'%22')
            soup = BeautifulSoup(r, 'lxml')
            if soup:
                link_list = []
                namelist = []
                more_records = True
                Round = False
                while more_records:
                    if Round:
                        response = br.follow_link(text="Next")
                        soup = BeautifulSoup(response)
                    # enter this loop to parse all results
                    # also follow any seondary links
                    for definition in soup.findAll('h2'):
                        definition = definition.renderContents()
                        if "LinkedIn" in definition:
                            name = (((((definition.replace('<strong>', '')).replace(
                                '</strong>', '')).split('>')[1]).split('|')[0]).rstrip()).split(',')[0]
                            name = name.split(' ')
                            if self.verbose:
                                e = ' [*] LinkedIn Name Found: ' + str(name)
                                print helpers.color(e, firewall=True)
                            namelist.append(name)
                    for link in br.links():
                        link_list.append(link.text)
                    if "Next" in link_list:
                        more_records = True
                        Round = True
                    else:
                        more_records = False
                if namelist:
                    return namelist
        except Exception as e:
            error = " [!] Major issue with Downloading LinkedIn source:" + \
                str(e)
            print helpers.color(error, warning=True)
        if namelist:
            return namelist

    def LinkedInClean(self, raw):
        '''
        This function simply uses clean names.
        '''
        try:
            if raw:
                firstname = raw[0]
                lastname = raw[1]
                try:
                    if "'" in firstname:
                        firstname = firstname.replace("'", "")
                    if "-" in firstname:
                        firstname = firstname.replace("-", "")
                    if " " in firstname:
                        firstname = firstname.replace(" ", "")
                    if "," in firstname:
                        firstname = firstname.replace(",", "")
                    if "(" in firstname:
                        firstname = firstname.replace("(", "")
                    if ")" in firstname:
                        firstname = firstname.replace(")", "")
                    if "'" in lastname:
                        lastname = lastname.replace("'", "")
                    if "-" in lastname:
                        lastname = lastname.replace("-", "")
                    if " " in lastname:
                        lastname = lastname.replace(" ", "")
                    if "," in lastname:
                        lastname = lastname.replace(",", "")
                    if "(" in lastname:
                        lastname = lastname.replace("(", "")
                    if ")" in lastname:
                        lastname = lastname.replace(")", "")
                    if ("@" in firstname) or ("@" in lastname):
                        return None
                except Exception as e:
                    pass
                try:
                    if raw[3]:
                        firstname = raw[0]
                        lastname = raw[3]
                        return [firstname, lastname]
                except Exception as e:
                    pass
                if self.verbose:
                    e = ' [*] Name Cleaned: ' + str([firstname, lastname])
                    print helpers.color(e, firewall=True)
                return [firstname, lastname]
        except Exception as e:
            if self.verbose:
                h = " [!] Error during name building: " + str(e)
                print helpers.color(h, warning=True)
            return None
