#!/usr/bin/env python
import helpers
import requests
import configparser
import Download

# Email layouts supported:
# {first}.{last} = alex.alex@domain.com
# {first}{last} = jamesharvey@domain.com
# {f}{last} = ajames@domain.com
# {f}.{last} = a.james@domain.com
# {first}{l} = jamesh@domain.com
# {first}.{l} = j.amesh@domain.com
# {first}_{last} = james_amesh@domain.com


class EmailFormat(object):

    '''
    A simple class to detect Email Format.
    Using basic checks and EmailHunter.
    '''

    def __init__(self, domain, Verbose=False):
        config = configparser.ConfigParser()
        try:
            config.read('Common/SimplyEmail.ini')
            self.UserAgent = str(config['GlobalSettings']['UserAgent'])
            self.apikeyv = str(config['APIKeys']['Hunter'])
            self.EmailType = str(config['Hunter']['EmailType'])
            self.domain = domain
            # self.email = email
            self.FinalAnswer = ''
            self.verbose = Verbose
            # If you send the exact same query twice, Hunter won't count the second request
            if self.EmailType == "Both":
                self.type = ""
                self.etype = "total"
            elif self.EmailType == "Personal":
                self.type = "&type=personal"
                self.etype = "personal_emails"
            elif self.EmailType == "Generic":
                self.type = "&type=generic"
                self.etype = "generic_emails"
        except Exception as e:
            print e

    def EmailHunterDetect(self):
        '''
        A function to use EmailHunter to use their
        JSON API to detect the email format.
        '''
        try:
            # This returns a JSON object
            dl = Download.Download(self.verbose)
            url = "https://api.hunter.io/v2/domain-search?domain=" + \
                self.domain + self.type + "&limit=100&offset=0" + "&api_key=" + self.apikeyv
            r = dl.requesturl(url, useragent=self.UserAgent, raw=True)
            results = r.json()
            pattern = str(results['data']['pattern'])
            if pattern:
                return pattern
            else:
                if self.verbose:
                    e = ' [!] No pattern detected via EmailHunter API'
                    print helpers.color(e, firewall=True)
                    return False
        except:
            error = "[!] Major issue with EmailHunter Search:" + str(e)
            print helpers.color(error, warning=True)

    def BuildName(self, CleanName, Format, Raw=False):
        '''
        Will help build names and return
        all required name formats for the email
        to be built.
        '''
        # Names are always [First, Last] List
        Name = ""
        try:
            FirstName = str(CleanName[0])
            FirstIntial = str(FirstName[0])
            LastName = str(CleanName[1])
            LastInitial = str(LastName[0])
        except:
            # not major if one name isnt built
            pass
        try:
            if Format == '{f}.{last}':
                Name = FirstIntial + '.' + LastName
            if Format == '{f}{last}':
                Name = FirstIntial + LastName
            if Format == '{first}{last}':
                Name = FirstName + LastName
            if Format == '{first}.{last}':
                Name = FirstName + '.' + LastName
            if Format == '{first}{l}':
                Name = FirstName + LastInitial
            if Format == '{first},{l}':
                Name = FirstName + '.' + LastInitial
            if Format == '{first}_{last}':
                Name = FirstName + "_" + LastName
            if Format == '{first}':
                Name = FirstName
        except:
            # not major if one name isnt built
            pass
        if Raw:
            return FirstName, FirstIntial, LastName, LastInitial
        if not Raw:
            return Name

    def EmailDetect(self, CleanNames, Domain, FinalEmails):
        '''
        if EmailHunterDetect cant find a
        format this function will build everytype of
        email and compare for a model.
        '''
        # Detect {f}{last} format
        FinalResult = []
        try:
            Set = False
            Format = '{f}{last}'
            for name in CleanNames:
                FirstName = str(name[0])
                FirstIntial = str(FirstName[0])
                LastName = str(name[1])
                self.BuildName
                BuiltEmail = FirstIntial + LastName + "@" + Domain
                # now use a list count method (Seems to be fater than nested
                # for loops)
                Count = FinalEmails.count(BuiltEmail.lower())
                if Count > 0:
                    if self.verbose:
                        r = " [*] Email format matched {f}{last}: " + \
                            BuiltEmail
                        print helpers.color(r, firewall=True)
                        if not Set:
                            FinalResult.append(Format)
                        Set = True
        except Exception as e:
            print e
        # Detect {f}.{last} format
        try:
            Set = False
            Format = '{f}.{last}'
            for name in CleanNames:
                FirstName = str(name[0])
                FirstIntial = str(FirstName[0])
                LastName = str(name[1])
                BuiltEmail = FirstIntial + '.' + LastName + "@" + Domain
                # now use a list count method (Seems to be fater than nested
                # for loops)
                Count = FinalEmails.count(BuiltEmail.lower())
                if Count > 0:
                    if self.verbose:
                        r = " [*] Email format matched {f}.{last}: " + \
                            BuiltEmail
                        print helpers.color(r, firewall=True)
                        if not Set:
                            FinalResult.append(Format)
                        Set = True
        except Exception as e:
            print e
        # Detect {first}{last}
        try:
            Set = False
            Format = '{first}{last}'
            for name in CleanNames:
                FirstName = str(name[0])
                LastName = str(name[1])
                BuiltEmail = FirstName + LastName + "@" + Domain
                # now use a list count method (Seems to be fater than nested
                # for loops)
                Count = FinalEmails.count(BuiltEmail.lower())
                if Count > 0:
                    if self.verbose:
                        r = " [*] Email format matched {first}{last}: " + \
                            BuiltEmail
                        print helpers.color(r, firewall=True)
                        if not Set:
                            FinalResult.append(Format)
                        Set = True
        except Exception as e:
            print e
        # Detect {first}.{last}
        try:
            Set = False
            Format = '{first}.{last}'
            for name in CleanNames:
                FirstName = str(name[0])
                LastName = str(name[1])
                BuiltEmail = FirstName + '.' + LastName + "@" + Domain
                # now use a list count method (Seems to be fater than nested
                # for loops)
                Count = FinalEmails.count(BuiltEmail.lower())
                if Count > 0:
                    if self.verbose:
                        r = " [*] Email format matched {first}.{last}: " + \
                            BuiltEmail
                        print helpers.color(r, firewall=True)
                        if not Set:
                            FinalResult.append(Format)
                        Set = True
        except Exception as e:
            print e
        # Detect {first}.{l}
        try:
            Set = False
            Format = '{first}.{l}'
            for name in CleanNames:
                FirstName = str(name[0])
                LastName = str(name[1])
                LastInitial = str(LastName[0])
                BuiltEmail = FirstName + '.' + LastInitial + "@" + Domain
                # now use a list count method (Seems to be fater than nested
                # for loops)
                Count = FinalEmails.count(BuiltEmail.lower())
                if Count > 0:
                    if self.verbose:
                        r = " [*] Email format matched {first}.{l}: " + \
                            BuiltEmail
                        print helpers.color(r, firewall=True)
                        if not Set:
                            FinalResult.append(Format)
                        Set = True
        except Exception as e:
            print e
        # Detect {first}{l}
        try:
            Set = False
            Format = '{first}{l}'
            for name in CleanNames:
                FirstName = str(name[0])
                LastName = str(name[1])
                LastInitial = str(LastName[0])
                BuiltEmail = FirstName + LastInitial + "@" + Domain
                # now use a list count method (Seems to be fater than nested
                # for loops)
                Count = FinalEmails.count(BuiltEmail.lower())
                if Count > 0:
                    if self.verbose:
                        r = " [*] Email format matched {first}{l}: " + \
                            BuiltEmail
                        print helpers.color(r, firewall=True)
                        if not Set:
                            FinalResult.append(Format)
                        Set = True
        except Exception as e:
            print e
        # Detect {first}.{last}
        try:
            Set = False
            Format = '{first}_{last}'
            for name in CleanNames:
                FirstName = str(name[0])
                LastName = str(name[1])
                BuiltEmail = FirstName + '_' + LastName + "@" + Domain
                # now use a list count method (Seems to be fater than nested
                # for loops)
                Count = FinalEmails.count(BuiltEmail.lower())
                if Count > 0:
                    if self.verbose:
                        r = " [*] Email format matched {first}_{last}: " + \
                            BuiltEmail
                        print helpers.color(r, firewall=True)
                        if not Set:
                            FinalResult.append(Format)
                        Set = True
        except Exception as e:
            print e
        try:
            Set = False
            Format = '{first}'
            for name in CleanNames:
                FirstName = str(name[0])
                LastName = str(name[1])
                BuiltEmail = FirstName + "@" + Domain
                # now use a list count method (Seems to be fater than nested
                # for loops)
                Count = FinalEmails.count(BuiltEmail.lower())
                if Count > 0:
                    if self.verbose:
                        r = " [*] Email format matched {first}: " + BuiltEmail
                        print helpers.color(r, firewall=True)
                        if not Set:
                            FinalResult.append(Format)
                        Set = True
        except Exception as e:
            print e
        # Finaly return the list of Formats
        # print FinalResult
        return FinalResult

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
                        BuiltName = str(
                            FirstIntial) + str(LastName) + "@" + Domain
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
                        BuiltName = str(FirstIntial) + '.' + \
                            str(LastName) + "@" + Domain
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
                print helpers.color(' [!] No names built, please do a sanity check!', warning=True)
                return False
        elif Format == '{first}{last}':
            for name in CleanNames:
                try:
                    FirstName = str(name[0])
                    LastName = str(name[1])
                    if FirstName and LastName:
                        # now build format
                        BuiltName = str(
                            FirstName) + str(LastName) + "@" + Domain
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
                print helpers.color(' [!] No names built, please do a sanity check!', warning=True)
                return False
        elif Format == '{first}.{last}':
            for name in CleanNames:
                try:
                    FirstName = str(name[0])
                    LastName = str(name[1])
                    if FirstName and LastName:
                        # now build foramt
                        BuiltName = str(
                            FirstName) + '.' + str(LastName) + "@" + Domain
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
                print helpers.color(' [!] No names built, please do a sanity check!', warning=True)
                return False
        elif Format == '{first}.{l}':
            for name in CleanNames:
                try:
                    FirstName = str(name[0])
                    LastName = str(name[1])
                    if FirstName and LastName:
                        # now build foramt
                        LastInitial = str(LastName[0])
                        BuiltName = str(FirstName) + '.' + \
                            str(LastInitial) + "@" + Domain
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
                print helpers.color(' [!] No names built, please do a sanity check!', warning=True)
                return False
        elif Format == '{first}{l}':
            for name in CleanNames:
                try:
                    FirstName = str(name[0])
                    LastName = str(name[1])
                    if FirstName and LastName:
                        # now build foramt
                        LastInitial = str(LastName[0])
                        BuiltName = str(
                            FirstName) + str(LastInitial) + "@" + Domain
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
                print helpers.color(' [!] No names built, please do a sanity check!', warning=True)
                return False
        elif Format == '{first}_{last}':
            for name in CleanNames:
                try:
                    FirstName = str(name[0])
                    LastName = str(name[1])
                    if FirstName and LastName:
                        # now build foramt
                        BuiltName = FirstName + "_" + LastName + "@" + Domain
                        if Verbose:
                            e = ' [*] Email built: ' + str(BuiltName)
                            print helpers.color(e, firewall=True)
                        if BuiltName:
                            BuiltEmails.append(BuiltName)
                except Exception as e:
                    print e
            if BuiltEmails:
                return BuiltEmails
        elif Format == '{first}':
            for name in CleanNames:
                try:
                    Name = self.BuildName(name, Format)
                    if Name:
                        # now build foramt
                        BuiltName = Name + "@" + Domain
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
                print helpers.color(' [!] No names built, please do a sanity check!', warning=True)
                return False
