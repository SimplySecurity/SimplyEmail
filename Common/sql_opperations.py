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

    def __init__(self, args=None):

        # init the class
        self.conn = self.database_connect()
        pass

    def database_connect(self):
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
    # domains will be a json blob of data
    
    def add_domain(self, domain):
        """
        add domain name to db
        for the first iteration.
        """
        last_scrapped = helpers.get_datetime()
        cur = self.conn.cursor()
        cur.execute("""INSERT INTO domain (domain,
                                            email_count,
                                            last_scrapped,
                                            instances_scraped,
                                            webmail,
                                            pattern,
                                            allows_verification) 
                    VALUES (?,?,?,?,?,?,?)""", (domain,0,last_scrapped,0,False,'',False))
        row_id = cur.lastrowid
        cur.close()
        return row_id

    def update_known_domain(self, domain):
        """
        add domain name to db
        for the first iteration.
        """

    def update_domain_count(self, domain):
        """
        a call that updates the domain 
        row with a proper email count.
        """
        row_id = self.get_domain_id(domain)
        count = self.get_domain_count(domain)
        cur = self.conn.cursor()
        cur.execute("UPDATE domain SET email_count = ? WHERE id=?", [count,row_id])
        cur.close()

    def get_domain_id(self, domain):
        """
        a call that updates the domain 
        row with a proper email count.
        """
        cur = self.conn.cursor()
        cur.execute("SELECT id FROM domain WHERE domain = ?", (domain,))
        count = cur.fetchone()[0]
        return count

    def get_domain_count(self, domain):
        """
        a call that gets the domain 
        row with a proper email count.
        """
        cur = self.conn.cursor()
        cur.execute("SELECT count(*) FROM email WHERE domain = ?", (domain,))
        count = cur.fetchone()[0]
        return count

    def get_domain_check(self, domain):
        """
        returns true or false if a emails is present in the DB.
        """
        # TODO: Fix this logic with tuples..
        cur = self.conn.cursor()
        cur.execute("SELECT id FROM domain WHERE domain = ?", (domain,))
        data = cur.fetchone()
        cur.close()
        try:
            if data == None:
                return False
            return True
        except:
            return True

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

    def get_email_check(self,email_address):
        """
        returns true or false if a emails is present in the DB.
        """
        # TODO: Fix this logic with tuples..
        cur = self.conn.cursor()
        cur.execute("SELECT id FROM email WHERE email_address = ?", (email_address,))
        data = cur.fetchone()
        cur.close()
        try:
            if data == None:
                return False
            return True
        except:
            return True

    def set_email(self,email_address,search_id,domain):
        """
        takes email blob and
        adds a email row.

        returns:
        email_id = the id unique to email for life
        """
        first_seen = helpers.get_datetime()
        cur = self.conn.cursor()
        cur.execute("""INSERT INTO email (email_address,
                                            domain,
                                            first_seen,
                                            last_seen,
                                            instances_seen,
                                            first_name,
                                            last_name,
                                            name_generated_email,
                                            email_verified,
                                            score) 
                    VALUES (?,?,?,?,?,?,?,?,?,?)""", (email_address,domain,first_seen,'',0,'','',False,False,0))
        row_id = cur.lastrowid
        cur.close()
        return row_id

    def update_known_email(self,email_address):
        last_seen = helpers.get_datetime()
        cur = self.conn.cursor()
        cur.execute("SELECT id FROM email WHERE email_address = ?", (email_address,))
        row_id = cur.fetchone()[0]
        cur.execute("SELECT instances_seen FROM email WHERE id = ?", (row_id,))
        instances_seen = cur.fetchone()[0]
        instances_seen += 1
        cur.execute("UPDATE email SET last_seen = ?, instances_seen = ? WHERE id=?", [last_seen, instances_seen, row_id])
        cur.close()
        return row_id

    def get_reporting_id(self):
        """
        takes a primay key id 
        and returns the reporting object.
        """

    def add_reporting(self, domain, modules_enabled=0):
        """
        takes required data type to set 
        up tasking in the db. 

        used at start of search
        returns: search_id 
        """
        search_id = helpers.get_searchid()
        cur = self.conn.cursor()
        cur.execute("""INSERT INTO reporting (search_id,
                                            domain, 
                                            start_time,
                                            end_time,
                                            modules_enabled_key,
                                            emails_found,
                                            emails_unique) 
                    VALUES (?,?,?,?,?,?,?)""", (search_id, domain, helpers.get_datetime(),'',0,0,0))
        cur.close()
        return search_id

    def update_reporting(self, emails_found, emails_unique, emails_domain, search_id):
        """
        update the reporting col 
        for the current task with the ending values
        """
        cur = self.conn.cursor()
        cur.execute("UPDATE reporting SET end_time = ?, emails_found = ?, emails_unique = ?, emails_domain = ? WHERE search_id=?", [helpers.get_datetime(), emails_found, emails_unique, emails_domain, search_id])
        cur.close()


    # def add_modules(self, search_id):
    #     """
    #     builds the intial row for the modules 
    #     table during reporting row creation.
    #     """
    #     f = False
    #     cur = self.conn.cursor()
    #     cur.execute("""INSERT INTO modules (search_id
    #                                         "ask_search" ,
    #                                         "canario_api" ,
    #                                         "cannary_search" ,
    #                                         "emailhunter_search" ,
    #                                         "exaled_doc" ,
    #                                         "exaled_docx" ,
    #                                         "exaled_pdf" ,
    #                                         "exaled_pptx" ,
    #                                         "exaled_search" ,
    #                                         "flickr_search" ,
    #                                         "github_code" ,
    #                                         "github_gist" ,
    #                                         "github_user" ,
    #                                         "google_csv" ,
    #                                         "google_doc" ,
    #                                         "google_docx" ,
    #                                         "google_pdf" ,
    #                                         "google_pptx" ,
    #                                         "google_search" ,
    #                                         "google_xlsx" ,
    #                                         "html_scrape" ,
    #                                         "oninstagram" ,
    #                                         "pastebin_search" ,
    #                                         "reddit_search" ,
    #                                         "pgp_search" ,
    #                                         "whois_api" ,
    #                                         "whoisolgy_search" ,
    #                                         "yahoo_search" 
    #                 VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""", (search_id,f,f,f,f,f,f,f,f,f,f,f,f,f,f,f,f,f,f,f,f,f,f,f,f,f,f,f,f)
    #     cur.close()





















