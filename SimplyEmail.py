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
from flask import Flask
from Helpers import helpers
from Helpers import VersionCheck
from Common import TaskController
from Common import sql_opperations
import sqlite3
import random
import string
import re
from flask import Flask, jsonify, abort, request, make_response, url_for

def database_connect():
    """
    Connect with the backend ./simplyemail.db sqlite database and return the
    connection object.
    """
    try:
        # set the database connectiont to autocommit w/ isolation level
        conn = sqlite3.connect('./data/simplyemail.db', check_same_thread=False)
        conn.text_factory = str
        conn.isolation_level = None
        return conn

    except Exception as e:
        print helpers.color("[!] Could not connect to database")
        print helpers.color("[!] Please run database_setup.py")
        sys.exit()

def execute_db_query(conn, query, args=None):
    """
    Execute the supplied query on the provided db conn object
    with optional args for a paramaterized query.
    """
    cur = conn.cursor()
    if(args):
        cur.execute(query, args)
    else:
        cur.execute(query)
    results = cur.fetchall()
    cur.close()
    return results    


def refresh_api_token(conn):
    """
    Generates a randomized RESTful API token and updates the value
    in the config stored in the backend database.
    """

    # generate a randomized API token
    apiToken = ''.join(random.choice(string.ascii_lowercase + string.digits) for x in range(40))

    execute_db_query(conn, "UPDATE config SET api_current_token=?", [apiToken])

    return apiToken


def get_permanent_token(conn):
    """
    Returns the permanent API token stored in SimplyEmail.db.
    If one doesn't exist, it will generate one and store it before returning.
    """

    permanentToken = execute_db_query(conn, "SELECT api_permanent_token FROM config")[0]
    if not permanentToken[0]:
        permanentToken = ''.join(random.choice(string.ascii_lowercase + string.digits) for x in range(40))
        execute_db_query(conn, "UPDATE config SET api_permanent_token=?", [permanentToken])

    return permanentToken[0]

####################################################################
#
# The SimplyEmail RESTful API.
# 
# ADAPTED FROM:
#       @HarmJ0y empire - EmPyre Rest API adapted with:
#       https://github.com/adaptivethreat/EmPyre/blob/master/empyre
#       http://blog.miguelgrinberg.com/post/designing-a-restful-api-with-python-and-flask
#       https://gist.github.com/miguelgrinberg/5614326
#
#    Verb     URI                                            Action
#    ----     ---                                            ------
#    GET      http://*:1337/api/version                     return the current SimplyEmail version
#    
#    GET      http://*:1337/api/config                      return the current default config
#
#    GET      http://*:1337/api/reporting                   returns all the search reports in the db
#    GET      http://*:1337/api/reporting/domain/TARGET.COM returns all the search reports in the db
#
#    GET      http://*:1337/api/domain                      return all the domains in DB 
#    GET      http://*:1337/api/domain/TARGET.COM           return JSON on TARGET.COM
#
#    GET      http://*:1337/api/email                       returns all the emails in the db
#    GET      http://*:1337/api/email/a@gmail.com           returns email data in JSON format for specfic email
#
#    GET      http://*:1337/api/execute(&type&domain&module)    executes a search via method
#    GET      http://*:1337/api/search
#
#    GET      http://*:1337/api/admin/login                 retrieve the API token given the correct username and password
#    GET      http://*:1337/api/admin/permanenttoken        retrieve the permanent API token, generating/storing one if it doesn't already exist
#    GET      http://*:1337/api/admin/shutdown              shutdown the RESTful API
#    GET      http://*:1337/api/admin/restart               restart the RESTful API
#    
####################################################################

def start_restful_api(startSimplyEmail=False, suppress=False, username=None, password=None, port=1337):
    """
    Kick off the RESTful API with the given parameters.
    startSimplyEmail -   start a complete startSimplyEmail in the backend as well
    suppress    -   suppress most console output
    username    -   optional username to use for the API, otherwise pulls from the SimplyEmail.db config
    password    -   optional password to use for the API, otherwise pulls from the SimplyEmail.db config
    port        -   port to start the API on, defaults to 1337 ;)
    """

    app = Flask(__name__)

    conn = database_connect()

    global serverExitCommand

    # if a username/password were not supplied, use the creds stored in the db
    (dbUsername, dbPassword) = execute_db_query(conn, "SELECT api_username, api_password FROM config")[0]

    if not username:
        username = dbUsername

    if not password:
        password = dbPassword

    print " * Starting RESTful API on port: %s" %(port)

    # refresh the token for the RESTful API
    apiToken = refresh_api_token(conn)
    print " * RESTful API token: %s" %(apiToken)

    permanentApiToken = get_permanent_token(conn)
    print " * Permanent API toeken : %s" %(permanentApiToken)
    tokenAllowed = re.compile("^[0-9a-z]{40}")

    oldStdout = sys.stdout
    if suppress:
        # suppress the normal Flask output
        log = logging.getLogger('werkzeug')
        log.setLevel(logging.ERROR)   

        # suppress all stdout and don't initiate the main cmdloop
        sys.stdout = open(os.devnull, 'w')

    # validate API token before every request except for the login URI
    @app.before_request
    def check_token():
        try:
            if request.path != '/api/admin/login':
                token = request.args.get('token')
                if (not token) or (not tokenAllowed.match(token)):
                    return make_response('', 401)
                if (token != apiToken) and (token != permanentApiToken):
                    return make_response('', 401)
                if request.remote_addr:
                    # log remote add to DB
                    s = sql_opperations.database()
                    s.add_request_log(request.remote_addr, token, request.base_url)
        except:
            return make_response(jsonify( { 'error': 'Unkown failure during auth' } ), 400)            

    @app.errorhandler(Exception)
    def exception_handler(error):
        return repr(error)


    @app.errorhandler(404)
    def not_found(error):
        return make_response(jsonify( { 'error': 'Not found' } ), 404)

    @app.errorhandler(410)
    def no_data(error):
        return make_response(jsonify( { 'error': 'No data to return' } ), 410)


    @app.route('/api/version', methods=['GET'])
    def get_version():
        """
        Returns the current SimplyEmail version.
        """
        config = configparser.ConfigParser()
        config.read('Common/SimplyEmail.ini')
        version = str(config['GlobalSettings']['Version'])
        return jsonify({'version': version})

    ###########################
    #                         #
    #   All meta functions    #
    #                         #  
    ###########################
    @app.route('/api/search/<string:domain_name>', methods=['GET'])
    def get_search_domain(domain_name):
        """
        Returns a search object for
        a domain from user.
        """
        s = sql_opperations.database()
        domain_dict = s.get_domain_email(domain_name)
        if domain_dict:
            return jsonify(domain_dict)
        else:
            return make_response(jsonify({'error': 'no data found for domain'}), 430)

    ###########################
    #                         #
    #  All execute functions  #
    #                         #  
    ###########################
    @app.route('/api/execute', methods=['POST'])
    def post_execute_command():
        """
        Returns a search object for
        a domain from user.

        takes:
        &type = bool for testing a module rather than full scrape
        &domain = the string of the domain to search
        """
        scrape_type = request.args.get('type')
        domain = request.args.get('domain')
        module = request.args.get('module')
        if scrape_type == 'test':
            Task = TaskController.Conducter()
            search_id = Task.TestModuleREST(domain, module)
            return jsonify({"search_id":search_id})
        else:
            return make_response(jsonify({'error': 'invalid api call (type missing)'}), 480)


    ###########################
    #                         #
    # All domain SQL functions#
    #                         #  
    ###########################

    @app.route('/api/domain', methods=['GET'])
    def get_domains():
        """
        Returns all the domains in the db.
        """
        try:
            s = sql_opperations.database()
            domain = s.get_domains()
            return jsonify({'domains': domain})
        except:
            return make_response(jsonify( { 'error': 'No data to return' } ), 410)
    
    @app.route('/api/domain/<string:domain_name>', methods=['GET'])
    def get_domain(domain_name):
        """
        Returns one domain in the db.
        """
        s = sql_opperations.database()
        row_id = s.get_domain_id(domain_name)
        if row_id:
            domain = s.get_domain(row_id)
            return jsonify({'domain': domain})
        else:
            return make_response(jsonify({'error': 'no domain found during query'}), 410)


    ###########################
    #                         #
    # All Email SQL functions #
    #                         #  
    ###########################

    @app.route('/api/email', methods=['GET'])
    def get_emails():
        """
        Returns all the domains in the db.
        """
        try:
            s = sql_opperations.database()
            emails = s.get_emails()
            return jsonify({'emails': emails})
        except:
            return make_response(jsonify({'error': 'no emails found during query'}), 410)


    @app.route('/api/email/<string:email_name>', methods=['GET'])
    def get_email(email_name):
        """
        Returns one domain in the db.
        """
        s = sql_opperations.database()
        row_id = s.get_email_id(email_name)
        if row_id:
            email = s.get_email(row_id)
            return jsonify({'email': email})
        else:
            return make_response(jsonify({'error': 'no domain found during query'}), 410)

    ###############################
    #                             #
    # All Reporting SQL functions #
    #                             #  
    ###############################

    @app.route('/api/reporting', methods=['GET'])
    def get_reporting():
        """
        Returns all search reports in the db.
        """
        try:
            s = sql_opperations.database()
            reports = s.get_reports()
            return jsonify({'reports': reports})
        except:
            return make_response(jsonify({'error': 'No data to return'}), 410)

    @app.route('/api/reporting/domain/<string:domain_name>', methods=['GET'])
    def get_reporting_domain(domain_name):
        """
        Returns all search reports for
        a domain provided.
        """
        s = sql_opperations.database()
        reports = s.get_reporting_domain(domain_name)
        if reports:
            return jsonify({'reports': reports})
        else:
            return make_response(jsonify({'error': 'no domain found during query'}), 410)


    context = ('./data/simplyemail.pem', './data/simplyemail.pem')
    app.run(host='0.0.0.0', port=port, ssl_context=context, threaded=True)


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
    parser.add_argument(
        '--rest', action='store_true', help='Run the SimplyEmail RESTful API.')
    parser.add_argument(
        '--suppress', default=False, action='store_true', help='Suppress the CLI output of SimplyEmail RESTful API.')
    parser.add_argument(
        '--restport', default=1337, help='Port to run the SimplyEmail RESTful API on.')
    parser.add_argument(
        '--username', help='Start the RESTful API with the specified username instead of pulling from SimplyEmail.db')
    parser.add_argument(
        '--password', help='Start the RESTful API with the specified password instead of pulling from SimplyEmail.db')
    
    parser.add_argument('-h', '-?', '--h', '-help',
                        '--help', action="store_true", help=argparse.SUPPRESS)
    args = parser.parse_args()
    if args.h:
        parser.print_help()
        sys.exit()
    return args.all, args.e, args.l, args.t, args.s, args.n, args.verify, args.v, args.json, args.rest, args.suppress, args.restport, args.username, args.password


def TaskStarter(version):
    # Get all the options passed and pass it to the TaskConducter, this will
    # keep all the processing on the side.
    # need to pass the store true somehow to tell printer to restrict output
    log = helpers.log()
    log.start()
    cli_all, cli_domain, cli_list, cli_test, cli_scope, cli_names, cli_verify, cli_verbose, cli_json, cli_rest, cli_suppress, cli_rport, cli_user, cli_pass = cli_parser()
    cli_domain = cli_domain.lower()
    Task = TaskController.Conducter()
    Task.load_modules()
    if cli_rest:
        start_restful_api(suppress=cli_suppress, username=cli_user, password=cli_pass, port=cli_rport)
        return
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
