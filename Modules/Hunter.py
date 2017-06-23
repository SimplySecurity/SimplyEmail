#!/usr/bin/env python
import configparser
import logging
from Helpers import Download
from Helpers import Parser
from Helpers import helpers

# Class will have the following properties:
# 1) name / description
# 2) main name called "ClassName"
# 3) execute function (calls everything it needs)
# 4) places the findings into a queue

# https://api.hunter.io/v2/domain-search?domain=any.com&type=personal&limit=100&offset=0&api_key=your_api_key


class ClassName(object):

    def __init__(self, domain, verbose=False):
        self.apikey = True
        self.name = "Hunter API"
        self.description = "Search the Hunter DB for potential emails"
        self.domain = domain
        config = configparser.ConfigParser()
        self.results = []
        self.verbose = verbose
        try:
            self.logger = logging.getLogger("SimplyEmail.Hunter")
            config.read('Common/SimplyEmail.ini')
            self.UserAgent = str(config['GlobalSettings']['UserAgent'])
            self.apikeyv = str(config['APIKeys']['Hunter'])
            self.RequestLimit = int(config['Hunter']['RequestLimit'])
            self.QuotaLimit = int(config['Hunter']['QuotaLimit'])
            self.EmailType = str(config['Hunter']['EmailType'])

            if self.EmailType == "Both":
                self.type = ""
                self.etype = "total"
            elif self.EmailType == "Personal":
                self.type = "&type=personal"
                self.etype = "personal_emails"
            elif self.EmailType == "Generic":
                self.type = "&type=generic"
                self.etype = "generic_emails"
            else:
                raise Exception("Email Type setting invalid")
        except Exception as e:
            self.logger.critical("Hunter module failed to __init__: " + str(e))
            print helpers.color(" [*] Error in Hunter settings: " + str(e) + "\n", warning=True)

    def execute(self):
        self.logger.debug("Hunter module started")
        self.process()
        FinalOutput, HtmlResults, JsonResults = self.get_emails()
        return FinalOutput, HtmlResults, JsonResults

    def process(self):
        dl = Download.Download(self.verbose)
        try:
            # We will check to see that we have enough requests left to make a search
            url = "https://api.hunter.io/v2/account?api_key=" + self.apikeyv
            r = dl.requesturl(url, useragent=self.UserAgent, raw=True)
            accountInfo = r.json()
            quota = int(accountInfo['data']['calls']['available'])
            quotaUsed = int(accountInfo['data']['calls']['used'])
            if quotaUsed >= self.QuotaLimit:
                overQuotaLimit = True
            else:
                overQuotaLimit = False
        except Exception as e:
            error = " [!] Hunter API error: " + str(accountInfo['errors'][0]['details'])
            print helpers.color(error, warning=True)      
        try:
            # Hunter's API only allows 100 emails per request, so we check the number of emails Hunter has 
            # on our specified domain, and if it's over 100 we need to make multiple requests to get all of the emails
            url = "https://api.hunter.io/v2/email-count?domain=" + self.domain
            r = dl.requesturl(url, useragent=self.UserAgent, raw=True)
            response = r.json()
            totalEmails = int(response['data'][self.etype])
            emailsLeft = totalEmails
            offset = 0
        except Exception as e:
            error = "[!] Major issue with Hunter Search: " + str(e)
            print helpers.color(error, warning=True)
        requestsMade = 0
        # Main loop to keep requesting the Hunter API until we get all of the emails they have
        while emailsLeft > 0:
            try:
                if overQuotaLimit or requestsMade + quotaUsed >= self.QuotaLimit:
                    if self.verbose:
                        print helpers.color(" [*] You are over your set Quota Limit: " + \
                            str(quotaUsed) + "/" + str(self.QuotaLimit) + " stopping search", firewall=True)
                    break
                elif self.RequestLimit != 0 and requestsMade >= self.RequestLimit:
                    if self.verbose:
                        print helpers.color(" [*] Stopping search due to user set Request Limit", firewall=True)
                    break

                # This returns a JSON object
                url = "https://api.hunter.io/v2/domain-search?domain=" + \
                    self.domain + self.type + "&limit=100&offset=" + str(offset) + "&api_key=" + self.apikeyv
                r = dl.requesturl(url, useragent=self.UserAgent, raw=True)
                results = r.json()
                emailCount = int(results['meta']['results'])
            except Exception as e:
                error = " [!] Hunter API error: " + str(results['errors'][0]['details']) + " QUITTING!"
                print helpers.color(error, warning=True)
                break
            try:
                # Make sure we don't exceed the index for the 'emails' array in the 'results' Json object
                if emailsLeft < 100:
                    emailCount = emailsLeft
                if emailCount > 100:
                    emailCount = 100
                # 1 request is every 10 emails delivered
                requestsMade += emailCount // 10
                if emailCount % 10 != 0:
                    requestsMade += 1
                # The API starts at 0 for the first value
                x = 0
                # We will itirate of the Json object for the index objects
                while x < emailCount:
                    self.results.append(results['data']['emails'][int(x)]['value'])
                    x += 1
                emailsLeft -= emailCount
                if emailsLeft > 100:
                    offset += 100
                else:
                    offset += emailsLeft
            except Exception as e:
                error = " [!] Major issue with search parsing: " + str(e)
                print helpers.color(error, warning=True)
                break
        if self.verbose:
            # Print the avalible requests user has if verbose
            print helpers.color(' [*] Hunter has completed JSON request', firewall=True)
            requestsUsed = requestsMade + quotaUsed
            if quota - requestsUsed <= 0:
                print helpers.color(" [*] You have no Hunter requests left." \
                    + "They will refill in about a month", firewall=True)
            else:
                print helpers.color(" [*] You have " + str(requestsUsed) \
                    + "/" + str(quota) + " Hunter requests left", firewall=True) 

    def get_emails(self):
        # Make sure you remove any newlines
        Parse = Parser.Parser(self.results)
        FinalOutput = Parse.CleanListOutput()
        HtmlResults = Parse.BuildResults(FinalOutput, self.name)
        JsonResults = Parse.BuildJson(FinalOutput, self.name)
        self.logger.debug('Hunter completed search')
        return FinalOutput, HtmlResults, JsonResults