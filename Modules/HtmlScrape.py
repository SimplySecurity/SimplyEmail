#!/usr/bin/env python

import subprocess
import configparser
import os
from Helpers import *


# Class will have the following properties:
# 1) name / description
# 2) main name called "ClassName"
# 3) execute function (calls everthing it neeeds)
# 4) places the findings into a queue

# Use the same class name so we can easily start up each module the same ways
class ClassName:

    def __init__(self, domain):
        # Descriptions that are required!!!
        self.name = "HTML Scape of Taget Website"
        self.description = "Html Scape the target website for emails and data"
        # Settings we will pull from config file (We need required options in
        # config file)
        config = configparser.ConfigParser()
        try:
            config.read('Common/SimplyEmail.ini')
            self.domain = domain
            self.useragent = "--user-agent=" + \
                str(config['GlobalSettings']['UserAgent'])
            self.depth = "--level=" + str(config['HtmlScrape']['Depth'])
            self.wait = "--wait=" + str(config['HtmlScrape']['Wait'])
            self.limit_rate = "--limit-rate=" + \
                str(config['HtmlScrape']['LimitRate'])
            self.timeout = "--read-timeout=" + \
                str(config['HtmlScrape']['Timeout'])
            self.save = "--directory-prefix=" + \
                str(config['HtmlScrape']['Save'])
        except:
            print helpers.color("[*] Major Settings for HTML are missing, EXITING!\n", warning=True)

    def execute(self):
        try:
            self.search()
            Emails = self.get_emails()
            return Emails
        except Exception as e:
            print e

    def search(self):
        try:
            # Using subprocess, more or less because of the rebust HTML miroring ability
            # And also allows proxy / VPN Support
            # "--convert-links"
            subprocess.call(["wget", "-q", self.save, "--header=""Accept: text/html""", self.useragent,
                             "--recursive", self.depth, self.wait, self.limit_rate,
                             self.timeout, "--page-requisites", "--html-extension", "--convert-links",
                             "-R gif,jpg,pdf,png", "--domains", self.domain, self.domain])
        except:
            print "[!] ERROR during Wget Request"

    def get_emails(self):
        # Direct location of new dir created during wget
        output = []
        FinalOutput = []
        directory = self.save.strip('--directory-prefix=') + self.domain
        # Grep for any data containing "@", sorting out binary files as well
        # Pass list of Dirs to a regex, and read that path for emails
        try:
            ps = subprocess.Popen(
                ('grep', '-r', "@", directory), stdout=subprocess.PIPE)
            # Take in "ps" var and parse it for only email addresses
            output = []
            val = subprocess.check_output(("grep", "-i", "-o", '[A-Z0-9._%+-]\+@[A-Z0-9.-]\+\.[A-Z]\{2,4\}'),
                                          stdin=ps.stdout)
            # Supper "hack" since the data returned is from Pipelin /n and all
            # in var
            with open('temp.txt', "wr+") as myfile:
                myfile.write(str(val))
            with open('temp.txt', "r") as myfile:
                output = myfile.readlines()
            os.remove('temp.txt')
            for item in output:
                FinalOutput.append(item.rstrip("\n"))
        except Exception as e:
            print e
            print "[!] ERROR during patern matching"
        # using PIPE output/input to avoid using "shell=True",
        # which can leave major security holes if script has certain permisions
        return FinalOutput
