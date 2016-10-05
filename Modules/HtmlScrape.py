#!/usr/bin/env python

import subprocess
import configparser
import os
import shutil
from Helpers import helpers
from Helpers import Parser


# Class will have the following properties:
# 1) name / description
# 2) main name called "ClassName"
# 3) execute function (calls everything it needs)
# 4) places the findings into a queue

# Use the same class name so we can easily start up each module the same ways
class ClassName(object):

    def __init__(self, domain, verbose=False):
        self.apikey = False
        # Descriptions are required!!!
        self.name = "HTML Scrape of Target Website"
        self.description = "Html Scrape the target website for emails and data"
        # Settings we will pull from config file (We need required options in
        # config file)
        config = configparser.ConfigParser()
        try:
            config.read('Common/SimplyEmail.ini')
            self.verbose = verbose
            self.domain = domain
            self.useragent = "--user-agent=\"" + str(config['GlobalSettings']['UserAgent']) + "\""
            self.depth = "--level=" + str(config['HtmlScrape']['Depth'])
            self.wait = "--wait=" + str(config['HtmlScrape']['Wait'])
            self.limit_rate = "--limit-rate=" + \
                str(config['HtmlScrape']['LimitRate'])
            self.timeout = "--timeout=" + \
                str(config['HtmlScrape']['Timeout'])
            self.save = "--directory-prefix=" + \
                str(config['HtmlScrape']['Save']) + str(self.domain)
            self.remove = str(config['HtmlScrape']['RemoveHTML'])
            self.retVal = 0
            self.maxRetries = "--tries=5"
        except:
            print helpers.color(" [*] Major Settings for HTML are missing, EXITING!\n", warning=True)

    def execute(self):
        try:
            self.search()
            FinalOutput, HtmlResults, JsonResults = self.get_emails()
            return FinalOutput, HtmlResults, JsonResults
        except Exception as e:
            print e

    def search(self):
        # setup domain so it will follow redirects
        # may move this to httrack in future
        TempDomain = "http://www." + str(self.domain)
        try:
            # Using subprocess, more or less because of the robust HTML mirroring ability
            # And also allows proxy / VPN Support
            # "--convert-links"
            if self.verbose:
                p = ' [*] HTML scrape underway [This can take a bit!]'
                print helpers.color(p, firewall=True)
            self.retVal = subprocess.call(["wget", "-q", "-e robots=off", "--header=\"Accept: text/html\"", self.useragent,
                             "--recursive", self.depth, self.wait, self.limit_rate, self.save,
                             self.timeout, "--page-requisites", "-R gif,jpg,pdf,png,css,zip,mov,wmv,ppt,doc,docx,xls,exe,bin,pptx,avi,swf,vbs,xlsx,kfp,pub",
                             "--no-clobber", self.maxRetries,"--domains", self.domain, TempDomain])
            if self.retVal > 0:
                print helpers.color(" [*] Wget returned error, likely 403 (attempting again): " + str(self.retVal), warning=True)
                self.retVal = subprocess.call(["wget", "-q", "-e robots=off", "--header=\"Accept: text/html\"", self.useragent,
                             "--recursive", self.depth, self.wait, self.limit_rate, self.save,
                             self.timeout, "--page-requisites", "-R gif,jpg,pdf,png,css,zip,mov,wmv,ppt,doc,docx,xls,exe,bin,pptx,avi,swf,vbs,xlsx,kfp,pub",
                             "--no-clobber", self.maxRetries,"--domains", self.domain, TempDomain])
        except Exception as e:
            print e
            print " [!] ERROR during Wget Request"

    def get_emails(self):
        # Direct location of new dir created during wget
        output = []
        FinalOutput = []
        val = ""
        directory = self.save.replace("--directory-prefix=", "")
        # directory = "www." + directory
        # Grep for any data containing "@", sorting out binary files as well
        # Pass list of Dirs to a regex, and read that path for emails
        try:
            if self.retVal > 0:
                pass
            else:
                ps = subprocess.Popen(
                    ('grep', '-r', "@", directory), stdout=subprocess.PIPE)
                # Take in "ps" var and parse it for only email addresses
                output = []
                try:
                    val = subprocess.check_output(("grep", "-i", "-o", '[A-Z0-9._%+-]\+@[A-Z0-9.-]\+\.[A-Z]\{2,4\}'),
                                                  stdin=ps.stdout)
                except Exception as e:
                    pass
                # Super "hack" since the data returned is from pipeline /n and all
                # in val
                if val:
                    with open('temp.txt', "w+") as myfile:
                        myfile.write(str(val))
                    with open('temp.txt', "r") as myfile:
                        output = myfile.readlines()
                    os.remove('temp.txt')
                    for item in output:
                        FinalOutput.append(item.rstrip("\n"))
        except Exception as e:
            print e
        if self.remove == "yes" or self.remove == "Yes":
            if not self.retVal > 0:
                shutil.rmtree(directory)
            try:
                shutil.rmtree(directory)
            except:
                pass
        Parse = Parser.Parser(FinalOutput)
        HtmlResults = Parse.BuildResults(FinalOutput, self.name)
        JsonResults = Parse.BuildJson(FinalOutput, self.name)
        return FinalOutput, HtmlResults, JsonResults
