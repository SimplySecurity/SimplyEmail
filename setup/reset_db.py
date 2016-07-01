#!/usr/bin/python

import sqlite3, os, string, hashlib
from Crypto.Random import random



# default credentials used to log into the RESTful API
API_USERNAME = "admin"
API_PASSWORD = 'password'

# the 'permanent' API token (doesn't change)
API_PERMANENT_TOKEN = ''.join(random.choice(string.ascii_lowercase + string.digits) for x in range(40))


###################################################
#
# Database setup.
#
###################################################


conn = sqlite3.connect('../data/simplyemail.db')

c = conn.cursor()

# try to prevent some of the weird sqlite I/O errors
c.execute('PRAGMA journal_mode = OFF')

c.execute('DROP TABLE IF EXISTS config')
c.execute('''CREATE TABLE config (
    "api_username" text,
    "api_password" text,
    "api_permanent_token" text
    )''')

# kick off the config component of the database
c.execute("INSERT INTO config VALUES (?,?,?)", (API_USERNAME, API_PASSWORD, API_PERMANENT_TOKEN))

# sources will be a json blob of data
c.execute('DROP TABLE IF EXISTS "email"')
c.execute('''CREATE TABLE "email" (
    "id" integer PRIMARY KEY,
    "email_address" text,
    "email_id" integer,
    "domain" text,
    "first_seen" text,
    "last_seen" text,
    "instances_seen" integer,
    "first_name" text,
    "last_name" text,
    "name_generated_email" boolean,
    "email_verified" boolean,
    "score" integer
    )''')

c.execute('DROP TABLE IF EXISTS "url"')
c.execute('''CREATE TABLE "url" (
    "id" integer PRIMARY KEY,
    "email_id" integer,
    "url" text,
    "datetime" text
    )''')

c.execute('DROP TABLE IF EXISTS "email_search_ids"')
c.execute('''CREATE TABLE "email_search_ids" (
    "id" integer PRIMARY KEY,
    "email_id" integer,
    "search_ids" text,
    "datetime" text
    )''')

# type = hash, plaintext, token
#   for tokens, the data is base64'ed and stored in pass
c.execute('DROP TABLE IF EXISTS "credentials"')
c.execute('''CREATE TABLE "credentials" (
    "id" integer PRIMARY KEY,
    "username" text,
    "password" text,
    "ip" text,
    "notes" text
    )''')


# event_types -> checkin, task, result, rename
# search_id = the search id will be used to link emails to searches etc
c.execute('DROP TABLE IF EXISTS "reporting"')
c.execute('''CREATE TABLE "reporting" (
    "id" integer PRIMARY KEY,
    "search_id" integer,
    "domain" text,
    "start_time" text,
    "end_time" text,
    "emails_found" integer,
    "modules_enabled_key" integer,
    "emails_unique" integer,
    "emails_domain" integer
    )''')

# domains will be a json blob of data
c.execute('DROP TABLE IF EXISTS "domain"')
c.execute('''CREATE TABLE "domain" (
    "id" integer PRIMARY KEY,
    "domain" text,
    "email_ids" text, 
    "email_count" integer,
    "urls" text,
    "last_scrapped" text,
    "search_ids" text,
    "webmail" boolean,
    "pattern" text,
    "allows_verification" boolean
    )''')


# table for modules used during search
c.execute('DROP TABLE IF EXISTS "modules"')
c.execute('''CREATE TABLE "modules" (
    "id" integer PRIMARY KEY,
    "search_id" integer,
    "ask_search" boolean,
    "canario_api" boolean,
    "cannary_search" boolean,
    "emailhunter_search" boolean,
    "exaled_doc" boolean,
    "exaled_docx" boolean,
    "exaled_pdf" boolean,
    "exaled_pptx" boolean,
    "exaled_search" boolean,
    "flickr_search" boolean,
    "github_code" boolean,
    "github_gist" boolean,
    "github_user" boolean,
    "google_csv" boolean,
    "google_doc" boolean,
    "google_docx" boolean,
    "google_pdf" boolean,
    "google_pptx" boolean,
    "google_search" boolean,
    "google_xlsx" boolean,
    "html_scrape" boolean,
    "oninstagram" boolean,
    "pastebin_search" boolean,
    "reddit_search" boolean,
    "pgp_search" boolean,
    "whois_api" boolean,
    "whoisolgy_search" boolean,
    "yahoo_search" boolean
    )''')


# commit the changes and close everything off
conn.commit()
conn.close()

print "\n [*] Database setup completed!\n"