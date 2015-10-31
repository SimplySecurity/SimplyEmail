#!/usr/bin/env python

import os
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
        # Major hack during testing;
        # I found grep is was better at Regex than re in python
        FinalOutput = []
        val = ""
        with open("temp-Output.temp", "wr") as myfile:
            myfile.write(self.InputData)
        ps = subprocess.Popen(
            ('grep', "@", "temp-Output.temp"), stdout=subprocess.PIPE)
        try:
            val = subprocess.check_output(("grep", "-i", "-o", '[A-Z0-9._%+-]\+@[A-Z0-9.-]\+\.[A-Z]\{2,4\}'),
                                          stdin=ps.stdout)
        except:
            pass
        os.remove('temp-Output.temp')
        if len(val) > 0:
            with open('temp.txt', "wr+") as myfile:
                myfile.write(str(val))
            with open('temp.txt', "wr+") as myfile:
                output = myfile.readlines()
            os.remove('temp.txt')
            for item in output:
                FinalOutput.append(item.rstrip("\n"))
        return FinalOutput
