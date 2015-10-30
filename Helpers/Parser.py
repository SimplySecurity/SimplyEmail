#!/usr/bin/env python

import string
import re
import subprocess

# Simple Parser Options for email enumeration.

# Taken from theHarvester


class Parser:

    def __init__(self, InputData):
        self.InputData = InputData
        #self.domain = domain

    def FindEmails(self):
        Result = []
        match = re.findall('[\w\.-]+@[\w\.-]+', self.InputData)
        for item in match:
            Result.append(item)
        #emails = self.unique()
        return Result

    def GrepFindEmails(self):
        with open("temp-Output.temp", "wr") as myfile:
            myfile.write(self.InputData)
        ps = subprocess.Popen(
            ('grep', '-r', "@", "temp-Output.temp"), stdout=subprocess.PIPE)
        val = subprocess.check_output(("grep", "-i", "-o", '[A-Z0-9._%+-]\+@[A-Z0-9.-]\+\.[A-Z]\{2,4\}'),
                                      stdin=ps.stdout)
        with open('temp.txt', "wr+") as myfile:
            myfile.write(str(val))
        with open('temp.txt', "r") as myfile:
            output = myfile.readlines()
        os.remove('temp.txt')
        for item in output:
            FinalOutput.append(item.rstrip("\n"))
        return FinalOutput
