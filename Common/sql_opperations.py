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


    #############################
    #                           #
    # logging table opperations #
    #                           #
    #############################

    def add_request_log(self, ipaddr, api_token, request):
        """
        adds row for authenticated request
        from API. 

        Takes:
        ip = ip from user
        token = api token of user
        request = full url request
        """
        ipaddr = str(ipaddr)
        api_token = str(api_token)
        request = str(request)
        datetime = helpers.get_datetime()
        cur = self.conn.cursor()
        cur.execute("""INSERT INTO logging (api_token,
                                    datetime,
                                    ipaddr,
                                    request) 
            VALUES (?,?,?,?)""", (api_token,datetime,ipaddr,request))
        cur.close()

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

    def get_domains(self):
        """
        a call that updates the domain 
        row with a proper email count.
        """
        final = []
        cur = self.conn.cursor()
        cur.execute("SELECT domain,email_count,last_scrapped,instances_scraped FROM domain")
        data = cur.fetchall()
        cur.close()
        for x in data:
            dic = {}
            dic['domain'] = x[0]
            dic['email_count'] = x[1]
            dic['last_scrapped'] = x[2]
            dic['instances_scraped'] = x[3]
            final.append(dic)
        return final

    def get_domain_id(self, domain):
        """
        a call that updates the domain 
        row with a proper email count.
        """
        cur = self.conn.cursor()
        cur.execute("SELECT id FROM domain WHERE domain = ?", (domain,))
        row_id = cur.fetchone()[0]
        cur.close()
        return row_id

    def get_domain(self, id_row):
        """
        a call that updates the domain 
        row with a proper email count.
        """
        cur = self.conn.cursor()
        cur.execute("SELECT domain,email_count,last_scrapped,instances_scraped FROM domain WHERE id = ?", (id_row,))
        data = cur.fetchone()
        cur.close()
        dic = {}
        dic['domain'] = data[0]
        dic['email_count'] = data[1]
        dic['last_scrapped'] = data[2]
        dic['instances_scraped'] = data[3]
        return dic

    def get_domain_count(self, domain):
        """
        a call that gets the domain 
        row with a proper email count.
        """
        cur = self.conn.cursor()
        cur.execute("SELECT count(*) FROM email WHERE domain = ?", (domain,))
        count = cur.fetchone()[0]
        cur.close()
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

    def get_email_id(self, email_name):
        """
        returns a email object with the 
        coresponding email db data.
        """
        cur = self.conn.cursor()
        cur.execute("SELECT id FROM email WHERE email_address = ?", (email_name,))
        row_id = cur.fetchone()[0]
        cur.close()
        return row_id

    def get_email(self, row_id):
        """
        returns a email objects in dict format
        """
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM email WHERE id = ?", (row_id,))
        x = cur.fetchone()
        cur.close()
        dic = {}
        dic['email_address'] = x[1]
        dic['domain'] = x[2]
        dic['first_seen'] = x[3]
        dic['last_seen'] = x[4]
        dic['instances_seen'] = x[5]
        dic['first_name'] = x[6]
        dic['last_name'] = x[7]
        dic['name_generated_email'] = x[8]
        dic['email_verified'] = x[9]
        dic['score'] = x[10]
        return dic

    def get_emails(self):
        """
        returns all emails in the DB and their objects.
        """
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM email")
        data = cur.fetchall()
        cur.close()
        final = []
        for x in data:
            dic = {}
            dic['email_address'] = x[1]
            dic['domain'] = x[2]
            dic['first_seen'] = x[3]
            dic['last_seen'] = x[4]
            dic['instances_seen'] = x[5]
            dic['first_name'] = x[6]
            dic['last_name'] = x[7]
            dic['name_generated_email'] = x[8]
            dic['email_verified'] = x[9]
            dic['score'] = x[10]
            final.append(dic)
        return final

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

    def get_reporting_id(self, search_id):
        """
        takes a primay key id 
        and returns the reporting object.
        """
        cur = self.conn.cursor()
        cur.execute("SELECT id FROM reporting WHERE search_id = ?", (search_id,))
        row_id = cur.fetchone()[0]
        cur.close()
        return row_id

    def get_reporting_domain(self, domain):
        """
        takes a domain and
        returns the reporting row_id(s).

        returns:
        row_id(s) = a list of row ideas for domain
        """
        cur = self.conn.cursor()
        cur.execute("SELECT id FROM reporting WHERE domain = ?", (domain,))
        data = cur.fetchall()
        cur.close()
        rows = []
        final = []
        for q in data:
            rows.append(q[0])
        for row_id in rows:
            final.append(self.get_report(row_id))
        return final

    def get_report(self,row_id):
        """
        pulls one search report 
        taking in a row_id for search
        """
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM reporting WHERE id = ?", (row_id,))
        x = cur.fetchone()
        cur.close()
        dic = {}
        dic['search_id'] = x[1]
        dic['domain'] = x[2]
        dic['start_time'] = x[3]
        dic['end_time'] = x[4]
        dic['emails_found'] = x[5]
        dic['modules_enabled_key'] = x[6]
        dic['emails_unique'] = x[7]
        dic['emails_domain'] = x[8]
        return dic


    def get_reports(self):
        """
        pulls all the search reports
        from the db.
        """
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM reporting")
        data = cur.fetchall()
        cur.close()
        final = []
        for x in data:
            dic = {}
            dic['search_id'] = x[1]
            dic['domain'] = x[2]
            dic['start_time'] = x[3]
            dic['end_time'] = x[4]
            dic['emails_found'] = x[5]
            dic['modules_enabled_key'] = x[6]
            dic['emails_unique'] = x[7]
            dic['emails_domain'] = x[8]
            final.append(dic)
        return final

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





















