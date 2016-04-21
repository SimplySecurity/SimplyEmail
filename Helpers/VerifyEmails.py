#!/usr/bin/env python
import configparser
import helpers
import dns.resolver
import socket
import smtplib


class VerifyEmail(object):

    '''
    Takes a domain name and an array of emails
    '''

    def __init__(self, email, email2, domain, Verbose=False):
        config = configparser.ConfigParser()
        try:
            config.read('Common/SimplyEmail.ini')
            self.UserAgent = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
            self.domain = domain
            self.email = email + email2
            self.mxhost = ""
            self.FinalList = []
            self.verbose = True
        except Exception as e:
            print e

    def VerifyEmail(self, email, email2):
        '''
        Takes one email and checks if it is valid.
        '''
        # Idea from:
        # https://www.scottbrady91.com/Email-Verification/Python-Email-Verification-Script
        hostname = socket.gethostname()
        socket.setdefaulttimeout(10)
        server = smtplib.SMTP(timeout=10)
        server.set_debuglevel(0)
        try:
            if self.verbose:
                e = " [*] Checking for valid email: " + str(email)
                print helpers.color(e, firewall=True)
            server.connect(self.mxhost['Host'])
            server.helo(hostname)
            server.mail('email@gmail.com')
            code, message = server.rcpt(str(email))
            server.quit()
        except Exception as e:
            print e
        if code == 250:
            return True
        else:
            return False

    def VerifySMTPServer(self):
        '''
        Checks for code other than 250 for crap email.
        '''
        # Idea from:
        # https://www.scottbrady91.com/Email-Verification/Python-Email-Verification-Script
        hostname = socket.gethostname()
        socket.setdefaulttimeout(10)
        server = smtplib.SMTP(timeout=10)
        server.set_debuglevel(0)
        addressToVerify = "There.Is.Knowwaythiswillwork1234567@" + \
            str(self.domain)
        try:
            server.connect(self.mxhost['Host'])
            server.helo(hostname)
            server.mail('email@gmail.com')
            code, message = server.rcpt(str(addressToVerify))
            server.quit()
            if code == 250:
                return False
            else:
                return True
        except Exception as e:
            print e

    def GetMX(self):
        MXRecord = []
        try:
            if self.verbose:
                print helpers.color(' [*] Attempting to resolve MX records!', firewall=True)
            answers = dns.resolver.query(self.domain, 'MX')
            for rdata in answers:
                data = {
                    "Host": str(rdata.exchange),
                    "Pref": int(rdata.preference),
                }
                MXRecord.append(data)
            # Now find the lowest value in the pref
            Newlist = sorted(MXRecord, key=lambda k: k['Pref'])
            # Set the MX record
            self.mxhost = Newlist[0]
            if self.verbose:
                val = ' [*] MX Host: ' + str(self.mxhost['Host'])
                print helpers.color(val, firewall=True)
        except Exception as e:
            error = ' [!] Failed to get MX record: ' + str(e)
            print helpers.color(error, warning=True)

    def ExecuteVerify(self):
        self.GetMX()
        Value = self.VerifySMTPServer()
        if Value:
            for item in self.email:
                IsTrue = self.VerifyEmail(item)
                if IsTrue:
                    e = " [!] Email seems valid: " + str(item)
                    print helpers.color(e, status=True)
                    self.FinalList.append(item)
                else:
                    if self.verbose:
                        e = " [!] Checks show email is not valid: " + str(item)
                        print helpers.color(e, firewall=True)
        else:
            e = " [!] Checks show 'Server Is Catch All' on: " + \
                str(self.mxhost['Host'])
            print helpers.color(e, warning=True)

        return self.FinalList
