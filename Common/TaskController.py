# -*- coding: utf-8 -*-
import configparser
import glob
import imp
import os
import multiprocessing
import threading
import sys
import warnings
import time
import subprocess
import logging
import datetime
# internal modules
from Helpers import helpers
from Helpers import messages
from Helpers import HtmlBootStrapTheme
from Helpers import VerifyEmails
from Helpers import Connect6
from Helpers import EmailFormat
from Helpers import LinkedinNames


class Conducter(object):

    # We are going to do the following in this order:
    # 1) Load Modules
    # 2) Add them to an array
    # 3) Task selector will take all those module names and place them into a
    #   queue
    # 4) The Threading function will call and pop from the queue and will
    #   instanciate that module
    # 5) The module will than can be dynamic in nature and we can add to the
    #   framework easily and effectily
    # 6) The module will place the results (emails) into a results queue in
    # memmory so we can output to Sqlite or WebPage or Console

    def __init__(self):
        # Create dictionaries of supported modules
        # empty until stuff loaded into them
        # stolen from Veil :)
        self.modules = {}
        self.dmodules = {}
        # create required array
        self.Emails = []
        self.ConsumerList = []
        self.HtmlList = []
        self.JsonList = []
        self.Tasks = []
        self.ResultsList = []
        self.search_id = 0
        self.logger = logging.getLogger("SimplyEmail.TaskController")
        try:
            config = configparser.ConfigParser()
            config.read('Common/SimplyEmail.ini')
            self.version = str(config['GlobalSettings']['Version'])
            self.logger.info("SimplyEmail Verison set to: " + self.version)
            # setup working dir for results
            t = datetime.datetime.now()
            self.TimeDate = str(t.strftime("%Y%m%d-%H%M"))
            self.logger.info("SimplyEmail started at: " + self.TimeDate)
        except Exception as e:
            print e

    # def TestModule(self, module, domain):
    #     ModuleName = module
    #     module = self.modules[module]
    #     module = module.ClassName(domain)
    #     name = " [*]" + module.name
    #     print name
    #     module.execute()

    def _execute_module_add_emails(self,Emails,Results_queue,Html_queue,Json_queue,HtmlResults,JsonResults):
        """
        Takes in queues and fills
        consumers with email data.
        """
        self.logger.debug("_execute_module_add_emails: adding emails to consumer qeues")
        for Email in Emails:
            Results_queue.put(Email)
        for Email in HtmlResults:
            Html_queue.put(Email)
        for Email in JsonResults:
            Json_queue.put(Email)
        self.logger.debug("_execute_module_add_emails: completed adding emails to consumer qeues")

    def _execute_api_module(self,Module):
        """
        Checks for API key in the 
        SimplyEmail.ini file.

        Module = Module handle to check
        """
        self.logger.debug("_execute_api_module: checking for API key")
        if Module.apikeyv:
            e = " [*] API module key loaded for: " + \
                Module.name
            print helpers.color(e, status=True)
            self.logger.info("_execute_api_module: API key present")
            return True
        else:
            e = " [*] No API module key loaded for: " + \
                Module.name
            print helpers.color(e, firewall=True)
            # Exit a API module with out a key
            self.logger.info("_execute_api_module: no API key present")
            return False

    def _execute_get_task(self, task_queue):
        """
        Takes in a m-queue to get 
        tasking and module to run.
        """
        try:
            task = task_queue.get()
            self.logger.debug("_execute_get_task: process requested tasking")
            return task
        except:
            self.logger.warning("_execute_get_task: task_queue.get() failed (unkown reason)")
            return None

    # Handler for each Process that will call all the modules in the Queue
    def ExecuteModule(self, Task_queue, Results_queue, Html_queue, Json_queue, domain, verbose=False):
        while True:
            Task = self._execute_get_task(Task_queue)
            if Task == None:
                self.logger.info("_execute_get_task: task_queue is empty (shutting down process)")
                break
            # Inst the class
            try:
                Task = self.modules[Task]
                Module = Task.ClassName(domain, verbose=verbose)
                name = " [*] Starting: " + Module.name
                print helpers.color(name, status=True)
                # Try to start the module
                try:
                    # Check for API key to ensure its in .ini
                    if Module.apikey:
                        if self._execute_api_module(Module) == False:
                            break
                    # Emails will be returned as a list
                    Emails, HtmlResults, JsonResults = Module.execute()
                    if Emails:
                        count = len(Emails)
                        self._execute_module_add_emails(Emails,Results_queue,Html_queue,Json_queue,HtmlResults,JsonResults)
                        count = len(Emails)
                        messages.email_count(count, Module.name)
                        # Task_queue.task_done()
                    else:
                        Message = " [*] " + Module.name + \
                            " has completed with no Email(s)"
                        print helpers.color(Message, status=True)
                except Exception as e:
                    error = " [!] Error During Runtime in Module " + \
                        Module.name + ": " + str(e)
                    print helpers.color(error, warning=True)
            except Exception as e:
                error = " [!] Error Loading Module: " + str(e)
                print helpers.color(error, warning=True)

    def printer(self, FinalEmailList, Domain, VerifyEmail=False, NameEmails=False):
        # Building out the Text file that will be outputted
        Date = time.strftime("%d/%m/%Y")
        Time = time.strftime("%I:%M:%S")
        buildpath = str(Domain) + "-" + self.TimeDate
        if not os.path.exists(buildpath):
            os.makedirs(buildpath)
        PrintTitle = "\t----------------------------------\n"
        PrintTitle += "\tEmail Recon: " + Date + " " + Time + "\n"
        PrintTitle += "\t----------------------------------\n"
        if NameEmails:
            x = 0
            NamePath = buildpath + "/Email_List_Built.txt"
            for item in FinalEmailList:
                item = item + "\n"
                if x == 0:
                    try:
                        with open(NamePath, "a") as myfile:
                            myfile.write(PrintTitle)
                    except Exception as e:
                        print e
                try:
                    with open(NamePath, "a") as myfile:
                        myfile.write(item)
                    x += 1
                except Exception as e:
                    print e
            print helpers.color(" [*] Completed output!", status=True)
            self.logger.info("Version / Update request started")
            return x
        elif VerifyEmail:
            x = 0
            VerPath = buildpath + "/Email_List_Verified.txt"
            for item in FinalEmailList:
                item = item + "\n"
                if x == 0:
                    try:
                        with open(VerPath, "a") as myfile:
                            myfile.write(PrintTitle)
                    except Exception as e:
                        print e
                try:
                    with open(VerPath, "a") as myfile:
                        myfile.write(item)
                    x += 1
                except Exception as e:
                    print e
            print helpers.color(" [*] Completed output!", status=True)
            return x
        else:
            x = 0
            ListPath = buildpath + "/Email_List.txt"
            for item in FinalEmailList:
                item = item + "\n"
                if x == 0:
                    try:
                        with open(ListPath, "a") as myfile:
                            myfile.write(PrintTitle)
                    except Exception as e:
                        print e
                try:
                    with open(ListPath, "a") as myfile:
                        myfile.write(item)
                    x += 1
                except Exception as e:
                    print e
            print helpers.color(" [*] Completed output!", status=True)
            return x

    def HtmlPrinter(self, HtmlFinalEmailList, Domain):
        # Builds the HTML file
        # try:
        self.logger.debug("HTML Printer started")
        buildpath = str(Domain) + "-" + self.TimeDate
        Html = HtmlBootStrapTheme.HtmlBuilder(HtmlFinalEmailList, Domain)
        Html.BuildHtml()
        Html.OutPutHTML(buildpath)
        # except Exception as e:
        # error =  "[!] Error building HTML file:" + e
        # print helpers.color(error, warning=True)

    def JsonPrinter(self, JsonFinalEmailList, FullPath, Domain):
        self.logger.debug("Json Printer started")
        json = helpers.JsonListToJsonObj(JsonFinalEmailList, Domain)
        if json:
            self.logger.debug("JSON data was returned")
            with open(str(FullPath), 'w') as file:
                file.write(json)
            self.logger.debug("JSON wrote file: " % (FullPath))


    def CleanResults(self, domain, scope=False):
        # Clean Up results, remove duplicates and enforce strict Domain results (future)
        # Set Timeout or you wont leave the While loop
        self.logger.debug("Clean Results started")
        SecondList = []
        HtmlSecondList = []
        # Validate the domain.. this can mess up but I dont want to miss
        # anything
        # scope will allow you to return all found emails
        # this will allow a user to scrape for all emails non related
        if scope:
            for item in self.ConsumerList:
                SecondList.append(item)
        else:
            for item in self.ConsumerList:
                if domain.lower() in helpers.split_email(item)[-1]:
                    SecondList.append(item)
        FinalList = []
        HtmlFinalList = []
        # now the same for Html Results with magic
        # scope will allow you to return all found emails
        # this will allow a user to scrape for all emails non related
        if scope:
            for item in self.HtmlList:
                HtmlSecondList.append(item)
        else:
            for item in self.HtmlList:
                if domain.lower() in helpers.split_email(item)[-1]:
                    HtmlSecondList.append(item)
        # Iter over all items in the list
        for item in SecondList:
            # Check if the value is in the new list
            if item.lower() not in FinalList:
                # Add item to list and put back in the Queue
                FinalList.append(item.lower())
                # results_queue.put(item)
        # Check to see we have dups (we will have dup emails)
        # But no Dup Sources (which we want)
        for item in HtmlSecondList:
            if item not in HtmlFinalList:
                HtmlFinalList.append(item)
        print helpers.color(" [*] Completed cleaning results", status=True)
        self.logger.info("Completed cleaning results")
        return FinalList, HtmlFinalList

    def CleanJsonResults(self, domain, scope=False):
        self.logger.debug("JSON Clean Results started")
        SecondList = []
        FinalList = []
        if scope:
            for item in self.JsonList:
                # add emails to sql db 
                SecondList.append(item)
        else:
            for item in self.JsonList:
                if domain.lower() in item['email'].lower():
                    # add scoped emails to sql db 
                    SecondList.append(item)
        for item in SecondList:
            if item not in FinalList:
                FinalList.append(item)
        return FinalList

    def Consumer(self, Results_queue, verbose):
        while True:
            try:
                item = Results_queue.get()
                if item is None:
                    break
                self.ConsumerList.append(item)
            except Exception as e:
                if verbose:
                    print e

    def HtmlConsumer(self, Html_queue, verbose):
        while True:
            try:
                item = Html_queue.get()
                if item is None:
                    break
                self.HtmlList.append(item)
            except Exception as e:
                if verbose:
                    print e

    def JsonConsumer(self, Json_queue, verbose):
        while True:
            try:
                item = Json_queue.get()
                if item is None:
                    break
                self.JsonList.append(item)
            except Exception as e:
                if verbose:
                    print e

    def _task_queue_start(self):
        """
        Private function to start task queue. 
        Allows for better debug.
        """
        self.logger.debug("_task_queue_start: starting task queue")
        try:
            Task_queue = multiprocessing.Queue()
            return Task_queue
        except:
            self.logger.critical("_task_queue_start: FAILED to start task_queue")

    def _results_queue_start(self):
        """
        Private function to start task queue. 
        Allows for better debug.
        """
        self.logger.debug("_results_queue_start: starting task queue")
        try:
            Results_queue = multiprocessing.Queue()
            return Results_queue
        except:
            self.logger.critical("_results_queue_start: FAILED to start Results_queue")

    def _html_queue_start(self):
        """
        Private function to start task queue. 
        Allows for better debug.
        """
        self.logger.debug("_html_queue_start: starting task queue")
        try:
            Html_queue = multiprocessing.Queue()
            return Html_queue
        except:
            self.logger.critical("_html_queue_start: FAILED to start Results_queue")

    def _json_queue_start(self):
        """
        Private function to start task queue. 
        Allows for better debug.
        """
        self.logger.debug("_json_queue_start: starting task queue")
        try:
            Json_queue = multiprocessing.Queue()
            return Json_queue
        except:
            self.logger.critical("_json_queue_start: FAILED to start Json_queue")

    def TaskSelector(self, domain, verbose=False, scope=False, Names=False, json="", Verify=False):
        # Here it will check the Queue for the next task to be completed
        # Using the Dynamic loaded modules we can easly select which module is up
        # Rather than using If statment on every task that needs to be done

        # Build our Queue of work for emails that we will gather
        self.logger.debug("Starting TaskSelector for: " + str(domain))
        Task_queue = self._task_queue_start()
        Results_queue = self._results_queue_start()
        Html_queue = self._html_queue_start()
        Json_queue = self._json_queue_start()

        # How many proc will we have, pull from config file, setting up the
        # config file handler
        Config = configparser.ConfigParser()
        Config.read("Common/SimplyEmail.ini")
        total_proc = int(Config['ProcessConfig']['TotalProcs'])
        self.logger.debug("TaskSelector processor set to: " + str(total_proc))
        # Place our email tasks in a queue
        for Task in self.modules:
            Task_queue.put(Task)
        # Make sure we aren't starting up Procs that aren't needed.
        if total_proc > len(self.modules):
            total_proc = len(self.modules)
        for i in xrange(total_proc):
            Task_queue.put(None)
            i = i
        procs = []
        for thread in range(total_proc):
            thread = thread
            procs.append(multiprocessing.Process(
                target=self.ExecuteModule, args=(Task_queue, Results_queue, Html_queue, Json_queue, domain, verbose)))
        for p in procs:
            p.daemon = True
            p.start()
        # This SAVED my life!
        # really important to understand that if the results queue was still full
        # the .join() method would not join even though a Consumer recived
        # a poison pill! This allows us to easily:
        # 1) start up all procs
        # 2) wait till all procs are posined
        # 3) than start up the cleaner and parser
        # 4) once finshed, than release by a break
        # 5) finally the Results_queue would be empty
        # 6) All procs can finally join!
        t = threading.Thread(target=self.Consumer, args=(Results_queue, verbose,))
        t.daemon = True
        t.start()
        # Start Html Consumer / Trying to keep these seperate
        t2 = threading.Thread(target=self.HtmlConsumer, args=(Html_queue, verbose,))
        t2.daemon = True
        t2.start()
        # Start Json Consumer
        t2 = threading.Thread(target=self.JsonConsumer, args=(Json_queue, verbose,))
        t2.daemon = True
        t2.start()
        # Enter this loop so we know when to terminate the Consumer thread
        # This multiprocessing.active_children() is also Joining!
        while True:
            LeftOver = multiprocessing.active_children()
            time.sleep(1)
            # We want to wait till we have no procs left, before we join
            if len(LeftOver) == 0:
                # Block until all results are consumed
                time.sleep(1)
                Results_queue.put(None)
                Html_queue.put(None)
                Json_queue.put(None)
                # t.join()
                try:
                    JsonFinalEmailList = self.CleanJsonResults(domain, scope)
                    FinalEmailList, HtmlFinalEmailList = self.CleanResults(
                        domain, scope)

                except Exception as e:
                    error = " [!] Something went wrong with parsing results:" + \
                        str(e)
                    print helpers.color(error, warning=True)
                    self.logger.critical("Something went wrong with parsing results: " + str(e))
                try:
                    if not json:
                        FinalCount = self.printer(FinalEmailList, domain)
                except Exception as e:
                    error = " [!] Something went wrong with outputixng results:" + \
                        str(e)
                    print helpers.color(error, warning=True)
                    self.logger.critical("Something went wrong with outputixng results: " + str(e))
                try:
                    if json:
                        self.JsonPrinter(JsonFinalEmailList, json, domain)
                    else:
                        self.HtmlPrinter(HtmlFinalEmailList, domain)
                except Exception as e:
                    error = " [!] Something went wrong with HTML results:" + \
                        str(e)
                    print helpers.color(error, warning=True)
                    self.logger.critical("Something went wrong with HTML results:: " + str(e))
                break
        for p in procs:
            p.join()
            self.logger.debug("TaskSelector processes joined!")
        Task_queue.close()
        Results_queue.close()
        Html_queue.close()
        Json_queue.close()
        BuiltNameCount = 0
        try:
            # If names is True
            if Names and not json:
                BuiltNames = self.NameBuilder(
                    domain, FinalEmailList, Verbose=verbose)
                BuiltNameCount = len(BuiltNames)
            if not Names:
                BuiltNames = []
            if Verify:
                val = self.VerifyScreen()
                if val:
                    email = VerifyEmails.VerifyEmail(
                        FinalEmailList, BuiltNames, domain)
                    VerifiedList = email.ExecuteVerify()
                    if VerifiedList:
                        self.printer(
                            FinalEmailList, domain, VerifyEmail=Verify)
                        # save seperate file for verified emails
        except Exception as e:
            print e
        try:
            if Names:
                if BuiltNames:
                    self.printer(BuiltNames, domain, NameEmails=True)
        except Exception as e:
            error = " [!] Something went wrong with outputting results of Built Names:" + \
                str(e)
            print helpers.color(error, warning=True)
        if not json:
            self.CompletedScreen(FinalCount, BuiltNameCount, domain)

    # This is the Test version of the multi proc above, this function
    # Helps with testing only one module at a time. Helping with proper
    # Module Dev and testing before integration
    def TestModule(self, domain, module, verbose=False, scope=False, Names=False, json='', Verify=False):
        self.logger.debug("Starting TaskSelector for: " + str(domain))
        Config = configparser.ConfigParser()
        Config.read("Common/SimplyEmail.ini")
        total_proc = int(1)
        self.logger.debug("Test TaskSelector processor set to: " + str(total_proc))
        Task_queue = self._task_queue_start()
        Results_queue = self._results_queue_start()
        Html_queue = self._html_queue_start()
        Json_queue = self._json_queue_start()

        for Task in self.modules:
            if module in Task:
                Task_queue.put(Task)
        # Only use one proc since this is a test module
        for i in xrange(total_proc):
            Task_queue.put(None)
        procs = []
        for thread in range(total_proc):
            procs.append(multiprocessing.Process(
                target=self.ExecuteModule, args=(Task_queue, Results_queue, Html_queue, Json_queue, domain, verbose)))
        for p in procs:
            p.daemon = True
            p.start()
        # This SAVED my life!
        # really important to understand that if the results queue was still full
        # the .join() method would not join even though a Consumer recived
        # a posin pill! This allows us to easily:
        # 1) start up all procs
        # 2) wait till all procs are posined
        # 3) than start up the cleaner and parser
        # 4) once finshed, than release by a break
        # 5) finally the Results_queue would be empty
        # 6) All procs can finally join!
        t = threading.Thread(target=self.Consumer, args=(Results_queue, verbose,))
        t.daemon = True
        t.start()
        # Start Html Consumer / Trying to keep these seprate
        t2 = threading.Thread(target=self.HtmlConsumer, args=(Html_queue, verbose,))
        t2.daemon = True
        t2.start()
        # Start Json Consumer
        t2 = threading.Thread(target=self.JsonConsumer, args=(Json_queue, verbose,))
        t2.daemon = True
        t2.start()
        # Enter this loop so we know when to terminate the Consumer thread
        # This multiprocessing.active_children() is also Joining!
        while True:
            LeftOver = multiprocessing.active_children()
            time.sleep(1)
            # We want to wait till we have no procs left, before we join
            if len(LeftOver) == 0:
                # Block until all results are consumed
                time.sleep(1)
                Results_queue.put(None)
                Html_queue.put(None)
                Json_queue.put(None)
                # t.join()
                try:
                    JsonFinalEmailList = self.CleanJsonResults(domain, scope)
                    FinalEmailList, HtmlFinalEmailList = self.CleanResults(
                        domain, scope)
                except Exception as e:
                    error = " [!] Something went wrong with parsing results:" + \
                        str(e)
                    print helpers.color(error, warning=True)
                    self.logger.critical("Something went wrong with parsing results: " + str(e))
                try:
                    if not json:
                        FinalCount = self.printer(FinalEmailList, domain)
                except Exception as e:
                    error = " [!] Something went wrong with outputting results:" + \
                        str(e)
                    print helpers.color(error, warning=True)
                    self.logger.critical("Something went wrong with outputting results: " + str(e))
                try:
                    if json:
                        self.JsonPrinter(JsonFinalEmailList, json, domain)
                    else:
                        self.HtmlPrinter(HtmlFinalEmailList, domain)
                except Exception as e:
                    error = " [!] Something went wrong with HTML results:" + \
                        str(e)
                    print helpers.color(error, warning=True)
                    self.logger.critical("Something went wrong with HTML results: " + str(e))
                # Check for valid emails if user wants
                break
        for p in procs:
            p.join()
        Task_queue.close()
        Results_queue.close()
        Html_queue.close()
        Json_queue.close()
        # Launches a single thread to output results
        BuiltNameCount = 0
        try:
            # If names is True
            if Names and not json:
                BuiltNames = self.NameBuilder(
                    domain, FinalEmailList, Verbose=verbose)
                BuiltNameCount = len(BuiltNames)
            if not Names:
                BuiltNames = []
            if not FinalEmailList:
                FinalEmailList = []
            if Verify:
                val = self.VerifyScreen()
                if val:
                    email = VerifyEmails.VerifyEmail(
                        FinalEmailList, BuiltNames, domain)
                    VerifiedList = email.ExecuteVerify()
                    if VerifiedList:
                        self.printer(
                            FinalEmailList, domain, VerifyEmail=Verify)
                        # save Seprate file for verified emails
        except Exception as e:
            print e
        try:
            if Names:
                if BuiltNames:
                    self.printer(BuiltNames, domain, NameEmails=True)
        except Exception as e:
            error = " [!] Something went wrong with outputting results of Built Names:" + \
                str(e)
            print helpers.color(error, warning=True)
        if not json:
            self.CompletedScreen(FinalCount, BuiltNameCount, domain)


    def NameBuilder(self, domain, emaillist, Verbose=False):
        '''
        Takes in Domain Names, returns List
        of names in indiviual lists.
        All the basic logic is here.
        '''
        self.logger.debug("Starting NameBuilder")
        self.title()
        ValidFormat = ['{first}.{last}', '{first}{last}', '{f}{last}',
                       '{f}.{last}', '{first}{l}', '{first}_{last}', '{first}']
        line = " [*] Now attempting to build Names:\n"
        print line
        CleanNames = []
        # Query for Linkedin Names - Adapted from
        # https://github.com/pan0pt1c0n/PhishBait
        self.logger.debug("Starting LinkedInScraper for names")
        Li = LinkedinNames.LinkedinScraper(domain, Verbose=Verbose)
        LNames = Li.LinkedInNames()
        if LNames:
            e = ' [*] LinkedinScraper has Gathered: ' + \
                str(len(LNames)) + ' Names'
            print helpers.color(e, status=True)
            self.logger.info("LinkedInScraper has Gathered: " + str(len(LNames)))
            for raw in LNames:
                try:
                    name = Li.LinkedInClean(raw)
                    if name:
                        CleanNames.append(name)
                except Exception as e:
                    print e
                    self.logger.error("Issue cleaning LinkedInNames: " + str(e))
        # Query for Connect6 Names
        c6 = Connect6.Connect6Scraper(domain, Verbose=Verbose)
        urllist = c6.Connect6AutoUrl()
        self.title()
        print helpers.color(" [*] Now Starting Connect6 Scrape:")
        self.logger.info("Now starting Connect6 scrape")
        if urllist:
            line = " [*] SimplyEmail has attempted to find correct URL for Connect6:\n"
            line += "     URL detected: " + \
                helpers.color(urllist[0], status=True)
            print line
            Question = " [>] Is this URL correct?: "
            Answer = raw_input(helpers.color(Question, bold=False))
            if Answer.upper() in "YES":
                Names = c6.Connect6Download(urllist[0])
                if Names:
                    e = ' [*] Connect6 has Gathered: ' + \
                        str(len(Names)) + ' Names'
                    print helpers.color(e, status=True)
                    for raw in Names:
                        name = c6.Connect6ParseName(raw)
                        if name:
                            CleanNames.append(name)
            else:
                while True:
                    for item in urllist:
                        print "    Potential URL: " + item
                    e = ' [!] GoogleDork This: site:connect6.com "' + \
                        str(domain)+'"'
                    print helpers.color(e, bold=False)
                    print " [-] Commands Supported: (B) ack - (R) etry"
                    Question = " [>] Please Provide a URL: "
                    Answer = raw_input(helpers.color(Question, bold=False))
                    if Answer.upper() in "BACK":
                        e = " [!] Skipping Connect6 Scrape!"
                        print helpers.color(e, firewall=True)
                        break
                    if Answer:
                        break
                if Answer.upper() != "B":
                    Names = c6.Connect6Download(Answer)
                    if Names:
                        e = ' [*] Connect6 has Gathered: ' + \
                            str(len(Names)) + ' Names'
                        print helpers.color(e, status=True)
                        for raw in Names:
                            name = c6.Connect6ParseName(raw)
                            if name:
                                CleanNames.append(name)
        else:
            line = " [*] SimplyEmail has attempted to find correct URL for Connect6:\n"
            line += "     URL was not detected!"
            print line
            e = ' [!] GoogleDork This: site:connect6.com "'+str(domain)+'"'
            print helpers.color(e, bold=False)
            while True:
                print " [-] Commands Supported: (B) ack - (R) etry"
                Question = " [>] Please Provide a URL: "
                Answer = raw_input(helpers.color(Question, bold=False))
                if Answer.upper() in "BACK":
                    e = " [!] Skipping Connect6 Scrape!"
                    print helpers.color(e, firewall=True)
                    break
                if Answer:
                    break
            if Answer.upper() != "B":
                Names = c6.Connect6Download(Answer)
                print Names
                if Names:
                    e = ' [*] Connect6 has Gathered: ' + \
                        str(len(Names)) + ' Names'
                    print helpers.color(e, status=True)
                    for raw in Names:
                        name = c6.Connect6ParseName(raw)
                        if name:
                            CleanNames.append(name)
        self.title()
        print helpers.color(' [*] Names have been built:', status=True)
        print helpers.color(' [*] Attempting to resolve email format', status=True)
        Em = EmailFormat.EmailFormat(domain, Verbose=Verbose)
        Format = Em.EmailHunterDetect()
        if Format:
            e = ' [!] Auto detected the format: ' + str(Format)
            print helpers.color(e, status=True)
        if not Format:
            print helpers.color(" [*] Now attempting to manually detect format (slow)!")
            Format = Em.EmailDetect(CleanNames, domain, emaillist)
            # Now check if we have more than one result in the list
            # This due to how I perform checks, in rare cases I had more than
            # one format.
            if len(Format) > 1:
                line = helpers.color(
                    ' [*] More than one email format was detected!\n')
                try:
                    for item in Format:
                        line += '   * Format: ' + item + '\n'
                    print line
                except:
                    p = " [*] No email samples gathered to show."
                    print helpers.color(p, firewall=True)
                line = ' [*] Here are a few samples of the emails obtained:\n'
                for i in range(1, 6, 1):
                    try:
                        line += '      %s) %s \n' % (i, emaillist[i])
                    except:
                        pass
                print line
                while True:
                    s = False
                    Question = " [>] Please provide a valid format: "
                    Answer = raw_input(helpers.color(Question, bold=False))
                    try:
                        for item in ValidFormat:
                            if str(Answer) == str(item):
                                Format = str(Answer)
                                s = True
                    except:
                        pass
                    if s:
                        break
            if len(Format) < 1:
                Format = False
            else:
                Format = str(Format[0])
        if not Format:
            print helpers.color(' [!] Failed to resolve format of email', firewall=True)
            line = helpers.color(
                ' [*] Available formats supported:\n', status=True)
            line += '     {first}.{last} = alex.alex@domain.com\n'
            line += '     {first}{last} = jamesharvey@domain.com\n'
            line += '     {f}{last} = ajames@domain.com\n'
            line += '     {f}.{last} = a.james@domain.com\n'
            line += '     {first}{l} = jamesh@domain.com\n'
            line += '     {first}.{l} = j.amesh@domain.com\n'
            line += '     {first}_{last} = james_amesh@domain.com\n'
            line += '     {first} = james@domain.com\n\n'
            print line
            if len(emaillist) > 0:
                line = ' [*] Here are a few samples of the emails obtained:\n'
                line += '      1)' + emaillist[0] + '\n'
                try:
                    if emaillist[1]:
                        line += '      2)' + emaillist[1] + '\n'
                    if emaillist[2]:
                        line += '      3)' + emaillist[2]
                except:
                    pass
                print line
            else:
                line = ' [*] No unique emails discovered to display (May have to go manual)!\n'
                print helpers.color(line, firewall=True)
            while True:
                s = False
                Question = " [>] Please provide a valid format: "
                Answer = raw_input(helpers.color(Question, bold=False))
                try:
                    for item in ValidFormat:
                        if str(Answer) == str(item):
                            Format = str(Answer)
                            s = True
                except:
                    pass
                if s:
                    break

        # Now build the emails!
        BuiltEmails = Em.EmailBuilder(
            CleanNames, domain, Format, Verbose=Verbose)
        if BuiltEmails:
            return BuiltEmails

    def load_modules(self):
        # loop and assign key and name
        warnings.filterwarnings('ignore', '.*Parent module*',)
        x = 1
        for name in glob.glob('Modules/*.py'):
            if name.endswith(".py") and ("__init__" not in name):
                loaded_modules = imp.load_source(
                    name.replace("/", ".").rstrip('.py'), name)
                self.logger.debug("Loading Module: " + str(loaded_modules))
                self.modules[name] = loaded_modules
                self.dmodules[x] = loaded_modules
                x += 1
        return self.dmodules
        return self.modules

    def ListModules(self):
        print helpers.color(" [*] Available Modules are:\n", blue=True)
        self.logger.debug("User Executed ListModules")
        x = 1
        ordList = []
        finalList = []
        for name in self.modules:
            parts = name.split("/")
            ordList.append(parts[-1])
        ordList = sorted(ordList)
        for name in ordList:
            name = 'Modules/' + name
            finalList.append(name)
        for name in finalList:
            print "\t%s)\t%s" % (x, '{0: <24}'.format(name))
            x += 1
        print ""

    def title(self):
        os.system('clear')
        # stolen from Veil :)
        self.logger.debug("Title executed")
        print " ============================================================"
        print " Current Version: " + self.version + " | Website: CyberSyndicates.com"
        print " ============================================================"
        print " Twitter: @real_slacker007 |  Twitter: @Killswitch_gui"
        print " ============================================================"

    def title_screen(self):
        self.logger.debug("Title_screen executed")
        offtext = """------------------------------------------------------------
   ______  ________                       __ __
 /      \/        |                     /  /  |
/$$$$$$  $$$$$$$$/ _____  ____   ______ $$/$$ |
$$ \__$$/$$ |__   /     \/    \ /      \/  $$ |
$$      \$$    |  $$$$$$ $$$$  |$$$$$$  $$ $$ |
 $$$$$$  $$$$$/   $$ | $$ | $$ |/    $$ $$ $$ |
/  \__$$ $$ |_____$$ | $$ | $$ /$$$$$$$ $$ $$ |
$$    $$/$$       $$ | $$ | $$ $$    $$ $$ $$ |
 $$$$$$/ $$$$$$$$/$$/  $$/  $$/ $$$$$$$/$$/$$/

------------------------------------------------------------"""
        print helpers.color(offtext, bold=False)

    def CompletedScreen(self, FinalCount, EmailsBuilt, domain):
        Config = configparser.ConfigParser()
        Config.read("Common/SimplyEmail.ini")
        TextSaveFile = str(Config['GlobalSettings']['SaveFile'])
        HtmlSaveFile = str(Config['GlobalSettings']['HtmlFile'])
        FinalEmailCount = int(EmailsBuilt) + int(FinalCount)

        Line = " [*] Email reconnaissance has been completed:\n\n"
        Line += "   File Location: \t\t" + \
            os.getcwd() + "/" + str(domain) + "-" + str(self.TimeDate) + "\n"
        Line += "   Unique Emails Found:\t\t" + str(FinalCount) + "\n"
        Line += "   Emails Built from Names:\t" + str(EmailsBuilt) + "\n"
        Line += "   Total Emails:\t\t" + str(FinalEmailCount) + "\n"
        Line += "   Raw Email File:\t\t" + str(TextSaveFile) + "\n"
        Line += "   HTML Email File:\t\t" + str(HtmlSaveFile) + "\n"
        Line += "   Built Email File:\t\tEmail_List_Built.txt\n"
        Line += "   Verified Email File:\t\tEmail_List_Verified.txt\n"
        Line += "   Domain Performed:\t\t" + str(domain) + "\n"
        self.title()
        print Line

        # Ask user to open report on CLI
        Question = "[>] Would you like to launch the HTML report?: "
        Answer = raw_input(helpers.color(Question, bold=False))
        Answer = Answer.upper()
        if Answer in "NO":
            sys.exit(0)
        if Answer in "YES":
            HtmlSaveFile = str(
                domain) + "-" + str(self.TimeDate) + "/" + HtmlSaveFile
            # gnome-open cisco.doc
            subprocess.Popen(
                ("firefox", HtmlSaveFile), stdout=subprocess.PIPE)

    def VerifyScreen(self):
        # Ask user to open report on CLI
        self.title()
        self.logger.debug("VerifyScreen executed")
        line = " [*] Email reconnaissance has been completed:\n\n"
        line += "    Email verification will allow you to use common methods\n"
        line += "    to attempt to enumerate if the email is valid.\n"
        line += "    This grabs the MX records, sorts and attempts to check\n"
        line += "    if the SMTP server sends a code other than 250 for known bad addresses\n"

        print line
        Question = " [>] Would you like to verify email(s)?: "
        Answer = raw_input(helpers.color(Question, bold=False))
        Answer = Answer.upper()
        if Answer in "NO":
            self.logger.info("User declined to run verify emails")
            return False
        if Answer in "YES":
            # gnome-open cisco.doc
            self.logger.info("User opted verify emails")
            return True
