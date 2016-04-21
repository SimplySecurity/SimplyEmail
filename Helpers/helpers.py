#!/usr/bin/env python

import os
import textwrap
import logging
import time
import magic
from fake_useragent import UserAgent


def color(string, status=True, warning=False, bold=True, blue=False, firewall=False):
    # Change text color for the linux terminal, defaults to green.
    # Set "warning=True" for red.
    # stolen from Veil :)
    attr = []
    if status:
        # green
        attr.append('32')
    if warning:
        # red
        attr.append('31')
    if bold:
        attr.append('1')
    if firewall:
        attr.append('33')
    if blue:
        # blue
        attr.append('34')
    return '\x1b[%sm%s\x1b[0m' % (';'.join(attr), string)


def formatLong(title, message, frontTab=True, spacing=16):
    """
    Print a long title:message with our standardized formatting.
    Wraps multiple lines into a nice paragraph format.
    """

    lines = textwrap.wrap(textwrap.dedent(message).strip(), width=50)
    returnstring = ""

    i = 1
    if len(lines) > 0:
        if frontTab:
            returnstring += "\t%s%s" % (('{0: <%s}' %
                                         spacing).format(title), lines[0])
        else:
            returnstring += " %s%s" % (('{0: <%s}' %
                                        (spacing-1)).format(title), lines[0])
    while i < len(lines):
        if frontTab:
            returnstring += "\n\t"+' '*spacing+lines[i]
        else:
            returnstring += "\n"+' '*spacing+lines[i]
        i += 1
    return returnstring


def DirectoryListing(directory):
    # Returns a list of dir's of results
    dirs = []
    for (dir, _, files) in os.walk(directory):
        for f in files:
            path = os.path.join(dir, f)
            if os.path.exists(path):
                dirs.append(path)
    return dirs


def getua():
    # gets a random useragent and returns the UA
    ua = UserAgent()
    return ua.random


def modsleep(st):
    # sleep module for spec time
    time.sleep(int(st))


def filetype(path):
    m = magic.from_file(str(path))
    return m

#######################
# Setup Logging Class #
#######################


class log(object):

    """simple logging testing and dev"""

    def __init__(self):
        self.name = ".SimplyEmail.log"

    def start(self):
        logger = logging.getLogger("SimplyEmail")
        logger.setLevel(logging.INFO)
        fh = logging.FileHandler(self.name)
        formatter = logging.Formatter(
            '%(asctime)s-[%(name)s]-[%(levelname)s]- %(message)s')
        fh.setFormatter(formatter)
        logger.addHandler(fh)
        logger.info("Program started")

    def infomsg(self, message, modulename):
        try:
            msg = 'SimplyEmail.' + str(modulename)
            logger = logging.getLogger(msg)
            logger.info(str(message))
        except Exception as e:
            print e

    def warningmsg(self, message, modulename):
        try:
            msg = 'SimplyEmail.' + str(modulename)
            logger = logging.getLogger(msg)
            logger.warning(str(message))
        except Exception as e:
            print e
