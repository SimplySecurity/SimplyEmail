#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Inspired by theHarvester and the capabilities. This project is simply a learning experience of
# recon methods to obtain email address and the way you can go about it.
# Also I really wanted the ability to learn SQL, and make this tool multi-threaded!
#
# * = Require API Key
#
import os
import argparse
import sys
import configparser
from Helpers import helpers
from Helpers import VersionCheck
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
    parser.add_argument(
        "-t", metavar="html / flickr / google", help="Test individual module (For Linting)")
    parser.add_argument(
        "-s", action='store_true', help="Set this to enable 'No-Scope' of the email parsing")
    parser.add_argument(
        "-n", action='store_true', help="Set this to enable Name Generation")
    parser.add_argument(
        "-verify", action='store_true', help="Set this to enable SMTP server email verify")
    parser.add_argument(
        "-v", action='store_true', help="Set this switch for verbose output of modules")
    parser.add_argument(
        "--json", metavar='json-emails.txt', default="", 
        help="Set this switch for json output to specfic file")
    parser.add_argument('-h', '-?', '--h', '-help',
                        '--help', action="store_true", help=argparse.SUPPRESS)
    args = parser.parse_args()
    if args.h:
        parser.print_help()
        sys.exit()
    return args.all, args.e, args.l, args.t, args.s, args.n, args.verify, args.v, args.json


def TaskStarter(version):
    # Get all the options passed and pass it to the TaskConducter, this will
    # keep all the processing on the side.
    # need to pass the store true somehow to tell printer to restrict output
    log = helpers.log()
    log.start()
    cli_all, cli_domain, cli_list, cli_test, cli_scope, cli_names, cli_verify, cli_verbose, cli_json = cli_parser()
    cli_domain = cli_domain.lower()
    Task = TaskController.Conducter()
    Task.load_modules()
    if cli_list:
        log.infomsg("Tasked to List Modules", "Main")
        Task.ListModules()
        V = VersionCheck.VersionCheck(version)
        V.VersionRequest()
        sys.exit(0)
    if not len(cli_domain) > 1:
        log.warningmsg("Domain not supplied", "Main")
        print helpers.color("[*] No Domain Supplied to start up!\n", warning=True)
        sys.exit(0)
    if cli_test:
        # setup a small easy test to activate certain modules
        log.infomsg("Tasked to Test Module: " + cli_test, "Main")
        V = VersionCheck.VersionCheck(version)
        V.VersionRequest()
        Task.TestModule(cli_domain, cli_test, verbose=cli_verbose,
                        scope=cli_scope, Names=cli_names, Verify=cli_verify, 
                        json=cli_json)
    if cli_all:
        log.infomsg("Tasked to run all Modules on domain: " + cli_domain, "Main")
        V = VersionCheck.VersionCheck(version)
        V.VersionRequest()
        Task.TaskSelector(cli_domain, verbose=cli_verbose,
                        scope=cli_scope, Names=cli_names, Verify=cli_verify, 
                        json=cli_json)


# def GenerateReport():
    # BootStrap with tables :)
    # Make a seprate reporting module fo sure way to busy here


def main():
    # instatiate the class
    try:
        config = configparser.ConfigParser()
        config.read('Common/SimplyEmail.ini')
        version = str(config['GlobalSettings']['Version'])
    except Exception as e:
        print e
    orc = TaskController.Conducter()
    orc.title()
    orc.title_screen()
    TaskStarter(version)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print 'Interrupted'
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
