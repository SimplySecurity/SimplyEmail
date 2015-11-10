#!/usr/bin/env python

import os
import re
import string
import subprocess
from random import randint

# Simple Parser Options for email enumeration.

# Taken from theHarvester


class Parser:

    def __init__(self, InputData):
        self.InputData = InputData
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

        for e in ('>', ':', '=', '<', '/', '\\', ';', '&', '%3A', '%3D', '%3C', '&#34'):
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
        StartFileName = randint(1000,999999)
        EndFileName = randint(1000,999999)
        val = ""
        with open(str(StartFileName), "wr") as myfile:
            myfile.write(self.InputData)
        ps = subprocess.Popen(
            ('grep', "@", str(StartFileName)), stdout=subprocess.PIPE)
        try:
            val = subprocess.check_output(("grep", "-i", "-o", '[A-Z0-9._%+-]\+@[A-Z0-9.-]\+\.[A-Z]\{2,4\}'),
                                          stdin=ps.stdout)
        except Exception as e:
            pass
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

    def CleanListOutput(self):
        FinalOutput = []
        for item in self.InputData:
            FinalOutput.append(item.rstrip("\n"))
        return FinalOutput
