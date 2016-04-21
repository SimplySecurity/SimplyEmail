#!/usr/bin/env python
import requests
import configparser
import helpers
import logging


class VersionCheck(object):

    def __init__(self, version):
        config = configparser.ConfigParser()
        try:
            self.logger = logging.getLogger("SimplyEmail.VersionCheck")
            self.version = str(version)
            config.read('Common/SimplyEmail.ini')
            self.Start = config['GlobalSettings']['VersionRepoCheck']
            self.RepoLocation = str(
                config['GlobalSettings']['VersionRepoCheckLocation'])
            self.UserAgent = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
        except Exception as e:
            print e

    def VersionRequest(self):
        if self.Start == "Yes":
            self.logger.info("Verison / Update request started")
            try:
                r = requests.get(self.RepoLocation, headers=self.UserAgent, timeout=3)
                results = r.content
                results = results.rstrip('\n')
                if str(results) != str(self.version):
                    p = " [!] Newer Version Available, Re-Run Setup.sh to update!"
                    print helpers.color(p, warning=True, bold=False)
                    self.logger.info(
                        "Version / Update returned newer Version Available")
                self.logger.info("Version / Update request completed OK")
            except Exception as e:
                error = " [!] Fail during Request to Update/Version Check (Check Connection)"
                self.logger.error(
                    "Fail during Request to Update/Version Check (Check Connection)" + str(e))
                print helpers.color(error, warning=True)
