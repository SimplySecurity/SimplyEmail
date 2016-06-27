#!/usr/bin/env python
# -*- coding: utf-8 -*-

import configparser
from Helpers import Parser
from Helpers import helpers
from Helpers import CanarioAPI

# Class will have the following properties:
# 1) name / description
# 2) main name called "ClassName"
# 3) execute function (calls everything it needs)
# 4) places the findings into a queue

# This method will do the following:
# 1) Get raw HTML for lets say enron.com )
#    This is mainly do to the API not supporting code searched with out known repo or user
#    :(https://canary.pw/search/?q=earthlink.net&page=3)
# 2) Use beautiful soup to parse the results of the first (5) pages for <A HREF> tags that start with "/view/"
# 3) Ueses a list of URL's and places that raw HTML into a on value
# 4) Sends to parser for results

# Some considerations are the returned results: max 100 it seems
# API may return a great array of results - This will be added later
# Still having some major python errors


class ClassName(object):

    def __init__(self, domain, verbose=False):
        self.apikey = True
        self.name = "Canar.io API PasteBin search"
        self.description = "Search Canar.io for paste potential data dumps, this can take a bit but a great source"
        self.domain = domain
        self.verbose = verbose
        config = configparser.ConfigParser()
        self.Html = ""
        try:
            config.read('Common/SimplyEmail.ini')
            self.Depth = int(config['CanaryPasteBin']['PageDepth'])
            self.Counter = int(config['CanaryPasteBin']['QueryStart'])
            self.apikeyv = str(config['APIKeys']['Canario'])
        except:
            print helpers.color(" [*] Major Settings for Canar.io Search are missing, EXITING!\n", warning=True)

    def execute(self):
        self.process()
        FinalOutput, HtmlResults, JsonResults = self.get_emails()
        return FinalOutput, HtmlResults, JsonResults

    def process(self):
        try:
            c = CanarioAPI.canary(api_key=str(self.apikeyv))
            s = c.search(self.domain)
            try:
                if str(s['data']['error_msg']):
                    error = str(s['data']['error_msg'])
                    e = " [!] Check your key and Canar.io limit: " + error
                    print helpers.color(e, warning=True)
            except:
                pass
            if str(s['action_valid']).lower() == 'true':
                if self.verbose:
                    print helpers.color(' [*] Canario query valid!')
                refid = []
                count = int(s['data']['results']['count'])
                if self.verbose:
                    e = ' [*] Canario result count: ' + str(count)
                    print helpers.color(e, firewall=True)
                if count > 0:
                    re = s['data']['results']['results']
                    # We need to make this a setting ?
                    for i in range(0, count, 1):
                        try:
                            result = re[i]
                            refid.append(str(result['referenceid']))
                        except Exception as e:
                            print e
                if len(refid) > 0:
                    # now enumerate the data in each refid
                    for ref in refid:
                        if self.verbose:
                            e = ' [*] Now enumerating refid: ' + str(ref)
                            print helpers.color(e, firewall=True)
                        try:
                            view = c.view(ref)
                            try:
                                emails = view['data']['objects']['email']
                                for em in emails:
                                    self.Html += str(em) + " "
                            except:
                                # just for weird cases where there is no
                                # values
                                pass
                            try:
                                body = view['data']['text_data']['body']
                                self.Html += str(body) + ' '
                            except:
                                # just for weird cases where there is no
                                # values
                                pass
                        except Exception as e:
                            p = " [!] Unable to enumerate Canario ref ID: " + \
                                str(e)
                            print helpers.color(p, warning=True)
            else:
                # logic to see if the key is bad
                print ""
        except Exception as e:
            l = ' [!] Check your Canario API key: ' + str(e)
            print helpers.color(l, warning=True)

    def get_emails(self):
        # You must report back with parsing errors!!!
        # in one case I have seen alex@gmail.com:Password
        # This will break most Reg-Ex
        Parse = Parser.Parser(self.Html)
        Parse.genericClean()
        Parse.urlClean()
        FinalOutput = Parse.GrepFindEmails()
        HtmlResults = Parse.BuildResults(FinalOutput, self.name)
        JsonResults = Parse.BuildJson(FinalOutput, self.name)
        return FinalOutput, HtmlResults, JsonResults
