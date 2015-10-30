#!/usr/bin/env python
import string
import httplib
import sys
import configparser
from Helpers import Parser
from Helpers import helpers

# Class will have the following properties:
# 1) name / description 
# 2) main name called "ClassName"
# 3) execute function (calls everthing it neeeds)
# 4) places the findings into a queue

class ClassName:

	def __init__(self, domain):
		self.name = "Searching PGP"
		self.description = "Search the PGP database for potential emails"
		self.domain = domain
		config = configparser.ConfigParser()
		self.results = ""
		try:
			config.read('Common/SimplyEmail.ini')
			self.server = str(config['SearchPGP']['KeyServer'])
			self.hostname = str(config['SearchPGP']['Hostname'])
			self.UserAgent = str(config['GlobalSettings']['UserAgent'])
		except:
			print helpers.color("[*] Major Settings for SearchPGP are missing, EXITING!\n", warning=True)

	def execute(self):
		self.process()
		FinalOutput = self.get_emails()
		return FinalOutput


	def process(self):
		h = httplib.HTTP(self.server)
		h.putrequest('GET', "/pks/lookup?search=" + self.domain + "&op=index")
		h.putheader('Host', self.hostname)
		h.putheader('User-agent', self.UserAgent)
		h.endheaders()
		returncode, returnmsg, headers = h.getreply()
		self.results = h.getfile().read()

	def get_emails(self):
		Parse = Parser.Parser(self.results)
		FinalOutput = Parse.FindEmails()
		return FinalOutput
