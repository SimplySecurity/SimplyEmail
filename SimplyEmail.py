#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Inspired by theHarvester and the capabilities. This project is simply a learning experience of
# recon methods to obtain email address and the way you can go about it.
# Also I really wanted the ability to learn SQL, and make this tool multipthreaded!
#
# * = Require API Key
#
# SimplyEmail v1.0 build out:
# (1) HTML Sraping
# (2) GoogleSearch
# (3) SEC Public Fillings*
# (4) PDF mining
import os
import argparse
import sys
from Helpers import helpers
from Common import TaskController


def cli_parser():
    parser = argparse.ArgumentParser(add_help=False, description='''
        Email enumeration is a important phase of so many operation that a pen-tester or\n
        Red Teamer goes through. There are tons of applications that do this but I wanted\n
        a simple yet effective way to get what Recon-Ng gets and theHarvester gets.\n 
        (You may want to run -h)
        ''')
    parser.add_argument(
        "-all", action='store_true', help="Use all non API methods to obtain Emails")
    parser.add_argument("-e", metavar="company.com", default="",
                        help="Set required email addr user, ex ale@email.com")
    parser.add_argument(
        "-l", action='store_true', help="List the current Modules Loaded")
    parser.add_argument('-h', '-?', '--h', '-help',
                        '--help', action="store_true", help=argparse.SUPPRESS)
    args = parser.parse_args()
    if args.h:
        parser.print_help()
        sys.exit()
    return args.all, args.e, args.l


def TaskControler():
    # Get all the options passed and pass it to the TaskConducter, this will
    # keep all the prcessing on the side.
    cli_all, cli_domain, cli_list = cli_parser()
    cli_domain = cli_domain.lower()
    if not len(cli_domain) > 1:
        print helpers.color("[*] No Domain Supplied to start up!\n", warning=True)
        sys.exit(0)

    # set up the clas
    Task = TaskController.Conducter()
    Task.load_modules()
    # List the current installed modules
    if cli_list:
        Task.ListModules()
        exit
    if cli_all:
        Task.TaskSelector(cli_domain)


# def GenerateReport():
    # BootStrap with tables :)
    # Make a seprate reporting module fo sure way to busy here


def main():
    # instatiate the class
    orc = TaskController.Conducter()
    orc.title()
    orc.title_screen()

    TaskControler()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print 'Interrupted'
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
