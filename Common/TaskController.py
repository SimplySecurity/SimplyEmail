# -*- coding: utf-8 -*-
import imp
import glob
import multiprocessing
import Queue
import configparser
import os
import warnings
from Helpers import helpers
from Helpers import HtmlBootStrapTheme


class Conducter:

    # We are going to do the following in this order:
    # 1) Load Modules
    # 2) Add them to an array
    # 3) Task selector will take all those module names and place them into a queue
    # 4) The Threading function will call and pop from the queue and will instanciate that module
    # 5) The module will than can be dynamic in nature and we can add to the framework easily and effectily
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
        self.Tasks = []
        self.version = "0.1"

    def ConfigSectionMap(section):
        dict1 = {}
        options = Config.options(section)
        for option in options:
            try:
                dict1[option] = Config.get(section, option)
                if dict1[option] == -1:
                    DebugPrint("skip: %s" % option)
            except:
                print("exception on %s!" % option)
                dict1[option] = None
        return dict1

    def TestModule(self, module, domain):
        ModuleName = module
        module = self.modules[module]
        module = module.ClassName(domain)
        name = "[*]" + module.name
        print name
        module.execute()

    # Handler for each Process that will call all the modules in the Queue
    def ExecuteModule(self, Task_queue, Results_queue, domain):
        while True:
            Task = Task_queue.get()
            # If the queue is emepty exit this proc
            if Task is None:
                break
            # Inst the class
            try:
                ModuleName = Task
                Task = self.modules[Task]
                Module = Task.ClassName(domain)
                name = "[*] Starting: " + Module.name
                print helpers.color(name, status=True)
                # Try to start the module
                try:
                    # Emails will be returned as a list
                    Emails = Module.execute()
                    if Emails:
                        count = len(Emails)
                        Length = "[*] " + Module.name + \
                            ": Gathered " + str(count) + " Email(s)!"
                        print helpers.color(Length, status=True)
                        for Email in Emails:
                            Results_queue.put(Email)
                        break
                    else:
                        Message = "[*] " + Module.name + " has completed with no Email(s)"
                        print helpers.color(Message, status=True)
                        break
                except Exception as e:
                    error = "[!] Error During Runtime in Module " + \
                        Module.name + ": " + str(e)
                    print helpers.color(error, warning=True)
            except Exception as e:
                error = "[!] Error Loading Module: " + str(e)
                print helpers.color(error, warning=True)

    def printer(self, results_queue):
        # Building out the Text file that will be outputted
        x = 0
        while True:
            # Get item an print to output file
            try:
                # Must set time out due to blocking,
                item = results_queue.get(timeout=1)
                item = item + "\n"
                with open('Email_list.txt', "a") as myfile:
                    myfile.write(item)
                    x += 1
            except Exception as e:
                print e
                break
            # results_queue.task_done()
        FinshText = "[* ]"
        print helpers.color("[*] Completed output!", status=True)
        return x

    def HtmlPrinter(self, FinalEmailList, Domain):
        # Builds the HTML file
        # try:
        Html = HtmlBootStrapTheme.HtmlBuilder(FinalEmailList, Domain)
        Html.BuildHtml()
        Html.OutPutHTML()
        # except Exception as e:
        #error =  "[!] Error building HTML file:" + e
        # print helpers.color(error, warning=True)

    def CleanResults(self, results_queue):
        # Clean Up results, remove dupplicates and enforce strict Domain reuslts (future)
        # Set Timeout or you wont leave the While loop
        EmailList = []
        while True:
            try:
                item = results_queue.get(timeout=1)
                EmailList.append(item)
            except Exception as e:
                print e
                break
        FinalList = []
        # Itt over all items in the list
        for item in EmailList:
            # Check if the value is in the new list
            if item not in FinalList:
                # Add item to list and put back in the Queue
                FinalList.append(item)
                results_queue.put(item)
        print helpers.color("[*] Completed Cleaning Results", status=True)
        return FinalList

    def TaskSelector(self, domain):
        # Here it will check the Que for the next task to be completed
        # Using the Dynamic loaded modules we can easly select which module is up
        # Rather than using If statment on every task that needs to be done

        # Build our Queue of work for emails that we will gather
        Task_queue = multiprocessing.Queue()
        Results_queue = multiprocessing.Queue()

        # How many proc will we have, pull from config file, setting up the
        # config file handler
        Config = configparser.ConfigParser()
        Config.read("Common/SimplyEmail.ini")
        total_proc = int(Config['ProcessConfig']['TottalProcs'])
        # Place our email tasks in a queue
        for Task in self.modules:
            Task_queue.put(Task)
        # Make sure we arnt starting up Procs that arnt needed.
        if total_proc > len(self.modules):
            total_proc = len(self.modules)
        for i in xrange(total_proc):
            Task_queue.put(None)
        procs = []
        for thread in range(total_proc):
            procs.append(multiprocessing.Process(
                target=self.ExecuteModule, args=(Task_queue, Results_queue, domain)))
        for p in procs:
            p.daemon = True
            p.start()
        for p in procs:
            p.join(timeout=60)
        # Launches a single thread to output results
        try:
            FinalEmailList = self.CleanResults(Results_queue)
        except Exception as e:
            error = "[!] Something went wrong with parsing results:" + str(e)
            print helpers.color(error, warning=True)
        try:
            FinalCount = self.printer(Results_queue)
        except Exception as e:
            error = "[!] Something went wrong with outputing results:" + str(e)
            print helpers.color(error, warning=True)
        try:
            self.HtmlPrinter(FinalEmailList, domain)
        except Exception as e:
            error = "[!] Something went wrong with HTML results:" + str(e)
            print helpers.color(error, warning=True)

        self.CompletedScreen(FinalCount, domain)

    def load_modules(self):
        # loop and assign key and name
        warnings.filterwarnings('ignore', '.*Parent module*',)
        x = 1
        for name in glob.glob('Modules/*.py'):
            if name.endswith(".py") and ("__init__" not in name):
                loaded_modules = imp.load_source(
                    name.replace("/", ".").rstrip('.py'), name)
                self.modules[name] = loaded_modules
                self.dmodules[x] = loaded_modules
                x += 1
        return self.dmodules
        return self.modules

    def ListModules(self):
        print helpers.color(" [*] Available Modules are:\n", blue=True)
        lastBase = None
        x = 1
        for name in self.modules:
            parts = name.split("/")
            if lastBase and parts[0] != lastBase:
                print ""
            lastBase = parts[0]
            print "\t%s)\t%s" % (x, '{0: <24}'.format(name))
            x += 1
        print ""

    # def module_menu(self, module):
 # int the Class Object
 #        module_name = module
 #        module = self.modules[module]
 #        module = module.ClassName()
 #        self.module_info(module)
 #        messages.helpmsg(self.modulescommands, showTitle=False)

    def title(self):
        os.system('clear')
        # stolen from Veil :)
        print " ============================================================"
        print " Curent Version: " + self.version + " | Website: Cyber-Syndicates.com"
        print " ============================================================"
        print " Twitter: @real_slacker007 |  Twitter: @Killswitch_gui"
        print " ============================================================"

    def title_screen(self):
        offtext = """-----------------------------------------------------------------------------
   ______  ________                       __ __ 
 /      \/        |                     /  /  |
/$$$$$$  $$$$$$$$/ _____  ____   ______ $$/$$ |
$$ \__$$/$$ |__   /     \/    \ /      \/  $$ |
$$      \$$    |  $$$$$$ $$$$  |$$$$$$  $$ $$ |
 $$$$$$  $$$$$/   $$ | $$ | $$ |/     $$ $$ $$ |
/  \__$$ $$ |_____$$ | $$ | $$ /$$$$$$$ $$ $$ |
$$    $$/$$       $$ | $$ | $$ $$    $$ $$ $$ |
 $$$$$$/ $$$$$$$$/$$/  $$/  $$/ $$$$$$$/$$/$$/

-----------------------------------------------------------------------------"""
        print helpers.color(offtext, bold=False)

    def CompletedScreen(self, FinalCount, domain):
        Config = configparser.ConfigParser()
        Config.read("Common/SimplyEmail.ini")
        TextSaveFile = str(Config['GlobalSettings']['SaveFile'])
        HtmlSaveFile = str(Config['GlobalSettings']['HtmlFile'])

        Line = " [*] Email reconnaissance has been completed:\n\n"
        Line += "   File Location: \t\t" + os.getcwd() + "\n"
        Line += "   Unique Emails Found:\t\t" + str(FinalCount) + "\n"
        Line += "   Raw Email File:\t\t" + str(TextSaveFile) + "\n"
        Line += "   HTML Email File:\t\t" + str(HtmlSaveFile) + "\n"
        Line += "   Domain Performed:\t\t" + str(domain) + "\n"
        self.title()
        print Line
