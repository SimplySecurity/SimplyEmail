#!/usr/bin/env python

import os, sys, types, string, textwrap

def color(string, status=True, warning=False, bold=True, blue=False):
    """
    Change text color for the linux terminal, defaults to green.
    Set "warning=True" for red.
    stolen from Veil :)
    """
    attr = []
    if status:
        # green
        attr.append('32')
    if warning:
        # red
        attr.append('31')
    if bold:
        attr.append('1')
    if blue:
        #blue
        attr.append('34')
    return '\x1b[%sm%s\x1b[0m' % (';'.join(attr), string)

def formatLong(title, message, frontTab=True, spacing=16):
    """
    Print a long title:message with our standardized formatting.
    Wraps multiple lines into a nice paragraph format.
    """

    lines = textwrap.wrap(textwrap.dedent(message).strip(), width=50)
    returnString = ""

    i = 1
    if len(lines) > 0:
        if frontTab:
            returnString += "\t%s%s" % (('{0: <%s}'%spacing).format(title), lines[0])
        else:
            returnString += " %s%s" % (('{0: <%s}'%(spacing-1)).format(title), lines[0])
    while i < len(lines):
        if frontTab:
            returnString += "\n\t"+' '*spacing+lines[i]
        else:
            returnString += "\n"+' '*spacing+lines[i]
        i += 1
    return returnString
    
def DirectoryListing(directory):
    # Returns a list of dir's of results
    dirs = []
    for (dir, _, files) in os.walk(directory):
        for f in files:
                path = os.path.join(dir, f)
                if os.path.exists(path):
                    dirs.append(path)      
    return dirs
