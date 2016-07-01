import logging
import sqlite3
import base64
import json
from Helpers import helpers


##########################################
# SQL opperations |  function
#   get_email()         performs all data extraction                 
#   set_email()         performs all data completions
#   search_email()      performs all email searches for common email ID keys
#   
#
#
#
#
##########################################



class database(object):

    _EMAIL_TABLE_COL = [
        'id',
        'email_address',
        'domain',
        'first_seen',
        'last_seen',
        'instances_seen',
        'sources',
        'first_name',
        'last_name',
        'name_generated_email',
        'email_verified',
        'score']

    _REPORTING_TABLE_COL = [
        "id",
        "search_id"             # TEXT - a built id of time
        "domain",               # TEXT - domain 
        "start_time",           # TEXT - start of the search
        "end_time",             # TEXT - end of successful search 
        "modules_enabled",      # TEXT - list of Modules being loaded
        "emails_found",         # INT - final count of emails (no scope)
        "emails_unique",        # INT - emails in the final count that are unique
        ]

    def __init__(self, MainMenu, args=None):

        # init the class
        self.conn = self.database_connect()
        pass

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
    ############################
    #                          #
    #  Meta functions for SQL  #
    #                          #
    ############################

    def build_search(self, domain, modules_enabled):
        """
        build the intial search options 
        for a scrape
        """
        search_id = self._add_reporting(domain, modules_enabled)
        self._add_modules(search_id)
        return search_id

    ############################
    #                          #
    #  Email table opperations #
    #                          #
    ############################

    def get_email_id(self, email_id):
        """
        returns a email object with the 
        coresponding email db data.
        """


    def get_emails(self):
        """
        returns all emails in the DB and their objects.
        """
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM email")
        results = cur.fetchall()
        cur.close()
        return results

    def set_email(self, email_json):
        """
        takes json email blob and
        adds a email row.
        """

    def get_reporting_id(self):
        """
        takes a primay key id 
        and returns the reporting object.
        """

    def _add_reporting(self, domain, modules_enabled):
        """
        takes required data type to set 
        up tasking in the db. 

        used at start of search
        returns: search_id 
        """
        search_id = helpers.get_searchid()
        cur = self.conn.cursor()
        cur.execute("""INSERT INTO reporting (search_id
                                            domain, 
                                            start_time,
                                            end_time,
                                            modules_enabled,
                                            emails_found,
                                            emails_unique) 
                    VALUES (?,?,?,?,?,?,?)""", (search_id, domain, helpers.get_datetime(),'',0,modules_enabled,0,0))
        cur.close()
        return search_id

    def update_reporting(self, emails_found, emails_unique):
        """
        update the reporting col 
        for the current task with the ending values
        """
        cur = self.conn.cursor()
        cur.close()


    def _add_modules(self, search_id):
        """
        builds the intial row for the modules 
        table during reporting row creation.
        """
        f = False
        cur = self.conn.cursor()
        cur.execute("""INSERT INTO modules (search_id
                                            "ask_search" ,
                                            "canario_api" ,
                                            "cannary_search" ,
                                            "emailhunter_search" ,
                                            "exaled_doc" ,
                                            "exaled_docx" ,
                                            "exaled_pdf" ,
                                            "exaled_pptx" ,
                                            "exaled_search" ,
                                            "flickr_search" ,
                                            "github_code" ,
                                            "github_gist" ,
                                            "github_user" ,
                                            "google_csv" ,
                                            "google_doc" ,
                                            "google_docx" ,
                                            "google_pdf" ,
                                            "google_pptx" ,
                                            "google_search" ,
                                            "google_xlsx" ,
                                            "html_scrape" ,
                                            "oninstagram" ,
                                            "pastebin_search" ,
                                            "reddit_search" ,
                                            "pgp_search" ,
                                            "whois_api" ,
                                            "whoisolgy_search" ,
                                            "yahoo_search" 
                    VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""", (search_id,f,f,f,f,f,f,f,f,f,f,f,f,f,f,f,f,f,f,f,f,f,f,f,f,f,f,f,f)
        cur.close()





















