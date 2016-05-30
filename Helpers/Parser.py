#!/usr/bin/env python
# encoding=utf8

import os
import re
import logging
import string
import subprocess
import time
from random import randint
import helpers

# Simple Parser Options for email enumeration.

# Taken from theHarvester


class Parser(object):

    def __init__(self, InputData):
        self.InputData = InputData
        self.logger = logging.getLogger("SimplyEmail.Parser")
        #self.domain = domain

    # A really good url clean by theHarvester at :
    # https://raw.githubusercontent.com/killswitch-GUI/theHarvester/master/myparser.py
    def genericClean(self):
        self.InputData = re.sub('<em>', '', self.InputData)
        self.InputData = re.sub('<b>', '', self.InputData)
        self.InputData = re.sub('</b>', '', self.InputData)
        self.InputData = re.sub('</em>', '', self.InputData)
        self.InputData = re.sub('%2f', ' ', self.InputData)
        self.InputData = re.sub('%3a', ' ', self.InputData)
        self.InputData = re.sub('<strong>', '', self.InputData)
        self.InputData = re.sub('</strong>', '', self.InputData)
        self.InputData = re.sub('<tr>', ' ', self.InputData)
        self.InputData = re.sub('</tr>', ' ', self.InputData)
        self.InputData = re.sub('</a>', ' ', self.InputData)

        for e in (',', '>', ':', '=', '<', '/', '\\', ';', '&', '%3A', '%3D', '%3C', '&#34', '"'):
            self.InputData = string.replace(self.InputData, e, ' ')

    # A really good url clean by theHarvester at :
    # https://raw.githubusercontent.com/killswitch-GUI/theHarvester/master/myparser.py
    def urlClean(self):
        self.InputData = re.sub('<em>', '', self.InputData)
        self.InputData = re.sub('</em>', '', self.InputData)
        self.InputData = re.sub('%2f', ' ', self.InputData)
        self.InputData = re.sub('%3a', ' ', self.InputData)
        for e in ('<', '>', ':', '=', ';', '&', '%3A', '%3D', '%3C'):
            self.InputData = string.replace(self.InputData, e, ' ')

    # http://stackoverflow.com/questions/32747648/
    # ascii-codec-cant-encode-character-u-u2019-ordinal-out-of-range128
    def RemoveUnicode(self):
        """ (str|unicode) -> (str|unicode)

        recovers ascii content from string_data
        """
        try:
            string_data = self.InputData
            if string_data is None:
                return string_data
            if isinstance(string_data, str):
                string_data = str(string_data.decode('ascii', 'ignore'))
            else:
                string_data = string_data.encode('ascii', 'ignore')
            remove_ctrl_chars_regex = re.compile(r'[^\x20-\x7e]')
            self.InputData = remove_ctrl_chars_regex.sub('', string_data)
        except Exception as e:
            self.logger.error('UTF8 decoding issues' + str(e))
            p = '[!] UTF8 decoding issues Matching: ' + str(e)
            print helpers.color(p, firewall=True)

    def FindEmails(self):
        Result = []
        match = re.findall('[\w\.-]+@[\w\.-]+', self.InputData)
        for item in match:
            Result.append(item)
        #emails = self.unique()
        return Result

    def GrepFindEmails(self):
        # Major hack during testing;
        # I found grep is was better at Regex than re in python
        FinalOutput = []
        StartFileName = randint(1000, 999999)
        EndFileName = randint(1000, 999999)
        val = ""
        try:
            with open(str(StartFileName), "w+") as myfile:
                myfile.write(self.InputData)
            ps = subprocess.Popen(
                ('grep', "@", str(StartFileName)), stdout=subprocess.PIPE)
            val = subprocess.check_output(("grep", "-i", "-o", '[A-Z0-9._%+-]\+@[A-Z0-9.-]\+\.[A-Z]\{2,4\}'),
                                          stdin=ps.stdout)
        # Start Email Evasion Check
        # This will be a seprate func to handle the lager sets of data
            EvasionVal = self.EmailEvasionCheck(ps)
        except Exception as e:
            pass
            #p = '[!] Pattern Matching Issue: ' + str(e)
            # print helpers.color(p, firewall=True)
        # Remove this line for Debuging pages
        os.remove(str(StartFileName))
        if len(val) > 0:
            with open(str(EndFileName), "w") as myfile:
                myfile.write(str(val))
            with open(str(EndFileName), "r") as myfile:
                output = myfile.readlines()
            os.remove(str(EndFileName))
            for item in output:
                FinalOutput.append(item.rstrip("\n"))
        return FinalOutput

    def EmailEvasionCheck(self, data):
        try:
            val = subprocess.check_output(("grep", "-i", "-o", '[A-Z0-9._%+-]\+\s+@+\s[A-Z0-9.-]\+\.[A-Z]\{2,4\}'),
                                          stdin=data.stdout)
        except:
            pass

    def CleanListOutput(self):
        FinalOutput = []
        for item in self.InputData:
            FinalOutput.append(item.rstrip("\n"))
        return FinalOutput

    def BuildResults(self, InputList, ModuleName):
        # Will use a generator expression to assign
        # emails to Keys and place into a list
        FinalOutput = []
        ModuleName = '"' + str(ModuleName) + '"'
        # build dict and append to list
        for email in InputList:
            email = '"' + str(email) + '"'
            ListItem = "{'Email': " + email + ", 'Source': " + ModuleName + "}"
            FinalOutput.append(ListItem)
        return FinalOutput

    def BuildJson(self, InputList, ModuleName):
        FinalOutput = []
        currentDate = str(time.strftime("%d/%m/%Y"))
        currentTime = str(time.strftime("%H:%M:%S"))
        moduleName = str(ModuleName)
        for email in InputList:
            obj = {
                'email': email,
                'module_name': moduleName,
                'collection_time': currentTime,
                'collection_data': currentDate,
            }
            FinalOutput.append(obj)
        # print FinalOutput
        return FinalOutput


    def extendedclean(self, modulename):
        self.genericClean()
        self.urlClean()
        finaloutput = self.GrepFindEmails()
        htmlresults = self.BuildResults(finaloutput, modulename)
        return finaloutput, htmlresults
