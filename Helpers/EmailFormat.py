#!/usr/bin/env python
import helpers
import requests
import configparser

'''
Email layouts supported:
  {first}.{last} = alex.alex@domain.com
  {first}{last} = jamesharvey@domain.com
  {f}{last} = ajames@domain.com
  {f}.{last} = a.james@domain.com
  {first}{l} = jamesh@domain.com
  {first}.{l} = j.amesh@domain.com
  {first}_{last} = james_amesh@domain.com

'''

class EmailFormat:
    '''
    A simple class to detect Email Format.
    Using basic checks and EmailHunter.
    '''
    def __init__(self, domain, Verbose=False):
      config = configparser.ConfigParser()
      try:
        config.read('Common/SimplyEmail.ini')
        self.UserAgent = {
          'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
        self.domain = domain
        # self.email = email
        self.FinalAnswer = ''
        self.verbose = Verbose
      except Exception as e:
        print e

    def EmailHunterDetect(self):
      '''
      A function to use EmailHunter to use their
      JSON API to detect the email format.
      '''
      try:
        # This returns a JSON object
        url = "https://emailhunter.co/trial/v1/search?offset=0&domain=" + \
            self.domain + "&format=json"
        r = requests.get(url)
      except Exception as e:
        error = "[!] Major issue with EmailHunter Search:" + str(e)
        print helpers.color(error, warning=True)
      try:
        results = r.json()
        # pprint(results)
        # Check to make sure we got data back from the API
        if results['status'] == "success":
          if results['pattern']:
            pattern = results['pattern']
            if pattern:
              return pattern
        else:
          if self.verbose:
            e = ' [!] No pattern dettected via EmailHunter API'
            print helpers.color(e, firewall=True)
            return False
      except:
        pass

    def EmailBuilder(self, CleanNames, Domain, Format, Verbose=True):
      '''
      Builds emails and returns a list of emails.
      '''
      BuiltEmails = []
      if len(CleanNames) < 0:
        return False
      if Format == '{f}{last}':
        for name in CleanNames:
          try:
            FirstName = str(name[0])
            LastName = str(name[1])
            if FirstName and LastName:
              # Build first intial
              FirstIntial = FirstName[0]
              # now build foramt
              BuiltName = str(FirstIntial) + str(LastName) + "@" + Domain
              if Verbose:
                e = ' [*] Email built: ' + str(BuiltName)
                print helpers.color(e, firewall=True)
              if BuiltName:
                BuiltEmails.append(BuiltName)
          except Exception as e:
            print e
        if BuiltEmails:
          return BuiltEmails
        else:
          print helpers.color(' [!] NO Names built, please do a sanity check!', warning=True)
          return False
      elif Format == '{f}.{last}':
        for name in CleanNames:
          try:
            FirstName = str(name[0])
            LastName = str(name[1])
            if FirstName and LastName:
              # Build first intial
              FirstIntial = FirstName[0]
              # now build foramt
              BuiltName = str(FirstIntial) + '.' + str(LastName) + "@" + Domain
              if Verbose:
                e = ' [*] Email built: ' + str(BuiltName)
                print helpers.color(e, firewall=True)
              if BuiltName:
                BuiltEmails.append(BuiltName)
          except Exception as e:
            print e
        if BuiltEmails:
          return BuiltEmails
        else:
          print helpers.color(' [!] NO Names built, please do a sanity check!', warning=True)
          return False
      elif Format == '{first}{last}':
        for name in CleanNames:
          try:
            FirstName = str(name[0])
            LastName = str(name[1])
            if FirstName and LastName:
              # now build foramt
              BuiltName = str(FirstName) + str(LastName) + "@" + Domain
              if Verbose:
                e = ' [*] Email built: ' + str(BuiltName)
                print helpers.color(e, firewall=True)
              if BuiltName:
                BuiltEmails.append(BuiltName)
          except Exception as e:
            print e
        if BuiltEmails:
          return BuiltEmails
        else:
          print helpers.color(' [!] NO Names built, please do a sanity check!', warning=True)
          return False
      elif Format == '{first}.{last}':
        for name in CleanNames:
          try:
            FirstName = str(name[0])
            LastName = str(name[1])
            if FirstName and LastName:
              # now build foramt
              BuiltName = str(FirstName) + '.' + str(LastName) + "@" + Domain
              if Verbose:
                e = ' [*] Email built: ' + str(BuiltName)
                print helpers.color(e, firewall=True)
              if BuiltName:
                BuiltEmails.append(BuiltName)
          except Exception as e:
            print e
        if BuiltEmails:
          return BuiltEmails
        else:
          print helpers.color(' [!] NO Names built, please do a sanity check!', warning=True)
          return False
      elif Format == '{first}.{l}':
        for name in CleanNames:
          try:
            FirstName = str(name[0])
            LastName = str(name[1])
            if FirstName and LastName:
              # now build foramt
              LastInitial = str(LastName[-1])
              BuiltName = str(FirstName) + '.' + str(LastInitial) + "@" + Domain
              if Verbose:
                e = ' [*] Email built: ' + str(BuiltName)
                print helpers.color(e, firewall=True)
              if BuiltName:
                BuiltEmails.append(BuiltName)
          except Exception as e:
            print e
        if BuiltEmails:
          return BuiltEmails
        else:
          print helpers.color(' [!] NO Names built, please do a sanity check!', warning=True)
          return False
      elif Format == '{first}{l}':
        for name in CleanNames:
          try:
            FirstName = str(name[0])
            LastName = str(name[1])
            if FirstName and LastName:
              # now build foramt
              LastInitial = str(LastName[-1])
              BuiltName = str(FirstName) + str(LastInitial) + "@" + Domain
              if Verbose:
                e = ' [*] Email built: ' + str(BuiltName)
                print helpers.color(e, firewall=True)
              if BuiltName:
                BuiltEmails.append(BuiltName)
          except Exception as e:
            print e
        if BuiltEmails:
          return BuiltEmails
        else:
          print helpers.color(' [!] NO Names built, please do a sanity check!', warning=True)
          return False
      elif Format == '{first}_{last}':
        for name in CleanNames:
          try:
            FirstName = str(name[0])
            LastName = str(name[1])
            if FirstName and LastName:
              # now build foramt
              BuiltName = str(FirstName) + "_" + str(LastName) + "@" + Domain
              if Verbose:
                e = ' [*] Email built: ' + str(BuiltName)
                print helpers.color(e, firewall=True)
              if BuiltName:
                BuiltEmails.append(BuiltName)
          except Exception as e:
            print e
        if BuiltEmails:
          return BuiltEmails
        else:
          print helpers.color(' [!] NO Names built, please do a sanity check!', warning=True)
          return False






