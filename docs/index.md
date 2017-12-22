[![Build Status](https://travis-ci.org/SimplySecurity/SimplyEmail.svg?branch=master)](https://travis-ci.org/SimplySecurity/SimplyEmail)
[![Code Health](https://landscape.io/github/SimplySecurity/SimplyEmail/master/landscape.svg?style=flat)](https://landscape.io/github/SimplySecurity/SimplyEmail/master)
[![Codacy Badge](https://api.codacy.com/project/badge/grade/3b8a338b659e425e9b4e1db9eace61d7)](https://www.codacy.com/app/iamfree2009/SimplyEmail)
[![Coverage Status](https://coveralls.io/repos/github/killswitch-GUI/SimplyEmail/badge.svg?branch=Version-1.4)](https://coveralls.io/github/killswitch-GUI/SimplyEmail?branch=Version-1.4)

![alt text](https://simplyemail.org/img/se-logo-2.png "Logo Title Text 1")

 # SimplyEmail
### https://simplyemail.org

What is the simple email recon tool? This tool was based off the work of theHarvester and kind of a port of the functionality. This was just an expansion of what was used to build theHarvester and will incorporate his work but allow users to easily build Modules for the Framework. Which I felt was desperately needed after building my first module for theHarvester.

MAJOR CALLOUTS:
- @laramies - Developer of theHarvester tool https://github.com/laramies/theHarvester
- @CptJesus - Helped dev framework


Work Conducted by:
----------------------------------------------
* Alexander Rymdeko-Harvey [Twitter] @Killswitch-GUI -- [Web] [CyberSydicates.com](http://cybersyndicates.com)
* Keelyn Roberts [Twitter] @real_slacker007 -- [Web] [CyberSydicates.com](http://cybersyndicates.com)

## Scrape EVERYTHING - Simply 

Current Platforms Supported:
* Kali Linux 2.0

A few small benefits:
- Easy for you to write modules (All you need is 1 required Class option and you're up and running)
- Use the built in Parsers for rawest results
- Multiprocessing Queue for modules and Result Queue for easy handling of Email data 
- Simple integration  of theHarvester Modules and new ones to come
- Also the ability to change major settings fast without diving into the code

API Based Searches:
- When API based searches become available, no need to add them to the Command line
- API keys will be auto pulled from the SimpleEmail.ini, this will activate the module for use
 
## Get Started in Kali
Install SimplyEmail in one line:
```
root@kali:~# curl -s https://raw.githubusercontent.com/killswitch-GUI/SimplyEmail/master/setup/oneline-setup.sh | bash
root@kali:~# cd SimplyEmail
(SE) root@kali:~/SimplyEmail# ./SimplyEmail.py

```
DONT trust a one line command no issue:
```
git clone --branch dev https://github.com/killswitch-GUI/SimplyEmail.git
cd SimplyEmail
./setup/setup.sh
cd ..
cd SimplyEmail
(SE) root@kali:~/SimplyEmail# ./SimplyEmail.py
```

NOTE: SimplyEmail uses autoenv to activate the Python Virtualenv.. It may prompt you the first time during a CD into the SimplyEmail dir.

## Get Started on Mac OSX 
```
Install brew:
https://coolestguidesontheplanet.com/installing-homebrew-on-os-x-el-capitan-10-11-package-manager-for-unix-apps/

$ sudo easy_install pip
$ sudo brew install libmagic
$ pip install python-magic
$ brew install autoenv
$ echo "source $(brew --prefix autoenv)/activate.sh" >> ~/.bash_profile
$ git clone --branch master https://github.com/killswitch-GUI/SimplyEmail.git
$ ./setup/setup.sh
```

### Standard Help
```
 ============================================================
 Current Version: v1.4.2 | Website: CyberSyndicates.com
 ============================================================
 Twitter: @real_slacker007 |  Twitter: @Killswitch_gui
 ============================================================
------------------------------------------------------------
   ______  ________                       __ __
 /      \/        |                     /  /  |
/$$$$$$  $$$$$$$$/ _____  ____   ______ $$/$$ |
$$ \__$$/$$ |__   /     \/    \ /      \/  $$ |
$$      \$$    |  $$$$$$ $$$$  |$$$$$$  $$ $$ |
 $$$$$$  $$$$$/   $$ | $$ | $$ |/    $$ $$ $$ |
/  \__$$ $$ |_____$$ | $$ | $$ /$$$$$$$ $$ $$ |
$$    $$/$$       $$ | $$ | $$ $$    $$ $$ $$ |
 $$$$$$/ $$$$$$$$/$$/  $$/  $$/ $$$$$$$/$$/$$/

------------------------------------------------------------
usage: SimplyEmail.py [-all] [-e company.com] [-l] [-t html / flickr / google]
                      [-s] [-n] [-verify] [-v] [--json json-emails.txt]

Email enumeration is a important phase of so many operation that a pen-tester
or Red Teamer goes through. There are tons of applications that do this but I
wanted a simple yet effective way to get what Recon-Ng gets and theHarvester
gets. (You may want to run -h)

optional arguments:
  -all                  Use all non API methods to obtain Emails
  -e company.com        Set required email addr user, ex ale@email.com
  -l                    List the current Modules Loaded
  -t html / flickr / google
                        Test individual module (For Linting)
  -s                    Set this to enable 'No-Scope' of the email parsing
  -n                    Set this to enable Name Generation
  -verify               Set this to enable SMTP server email verify
  -v                    Set this switch for verbose output of modules
  --json json-emails.txt
                        Set this switch for json output to specfic file
```

### Run SimplyEmail

Let's say your target is cybersyndicates.com
```python
./SimplyEmail.py -all -e cybersyndicates.com

or in verbose
./SimplyEmail.py -all -v -e cybersyndicates.com

or in verbose and no "Scope"
./SimplyEmail.py -all -v -e cybersyndicates.com -s

or with email verification
./SimplyEmail.py -all -v -verify -e cybersyndicates.com 

or with email verification & Name Creation
./SimplyEmail.py -all -v -verify -n -e cybersyndicates.com 

or json automation
./SimplyEmail.py -all -e cybersyndicates.com --json cs-json.txt
```
This will run ALL modules that are have API Key placed in the SimpleEmail.ini file and will run all non-API based modules. 

### List Modules SimpleEmail
Current modules:

	1)	Modules/AskSearch.py    
	2)	Modules/CanarioAPI.py **(Deprecated)**   
	3)	Modules/CanaryBinSearch.py **(Deprecated)**
	4)	Modules/EmailHunter.py  
	5)	Modules/ExaleadDOCSearch.py
	6)	Modules/ExaleadDOCXSearch.py
	7)	Modules/ExaleadPDFSearch.py
	8)	Modules/ExaleadPPTXSearch.py
	9)	Modules/ExaleadSearch.py
	10)	Modules/ExaleadXLSXSearch.py
	11)	Modules/FlickrSearch.py 
	12)	Modules/GitHubCodeSearch.py
	13)	Modules/GitHubGistSearch.py
	14)	Modules/GitHubUserSearch.py
	15)	Modules/GoogleCsvSearch.py
	16)	Modules/GoogleDocSearch.py
	17)	Modules/GoogleDocxSearch.py
	18)	Modules/GooglePDFSearch.py
	19)	Modules/GooglePPTXSearch.py
	20)	Modules/GoogleSearch.py 
	21)	Modules/GoogleXLSXSearch.py
	22)	Modules/HtmlScrape.py   
	23)	Modules/PasteBinSearch.py
	24)	Modules/RedditPostSearch.py
	25)	Modules/SearchPGP.py    
	26)	Modules/WhoisAPISearch.py
	27)	Modules/Whoisolgy.py    
	28)	Modules/YahooSearch.py 

## API Modules and Searches
API based searches can be painful and hard to configure. The main aspect of SimplyEmail is to easily integrate these aspects, while not compromising the ease of using this tool. Using the configuration file, you can simply add your corresponding API key and get up and running. Modules are automatically identified as API based searches, checks if the corresponding keys are present and if the keys are present it will run the module. 

### Canar.io API Search
Canario is a service that allows you to search for potentially leaked data that has been exposed on the Internet. Passwords, e-mail addresses, hostnames, and other data have been indexed to allow for easy searching.

Simply Register for a key here:
[canar.io] (https://canar.io/register/) or https://canar.io/register/
Place the key in the SimplyEmail.ini at [APIKeys] section, the module will now initiate when the --all flag is user of the -t.


## Name Generation
Some times SimplyEmail will only find the standard email addresses or just a few emails. In this case email creation may be your saving grace. Using name generation can allow you not only scrape names from diffrent sites but allow you to auto detect the format to some accuracy. 

### LinkedIn Name Generation
Using Bing and work from PhishBait I was able to implement LinkedIn name lookups from the company name. 

### Connect6.com Name Generation
Connect6 is also a great source for names, and also a bit flaky to find the source. Using a AutoUrl function I built I do attempt to find the correct URL for you. If not I provide you with a few more to pick from.

```
 ============================================================
 Current Version: v1.1 | Website: CyberSyndicates.com
 ============================================================
 Twitter: @real_slacker007 |  Twitter: @Killswitch_gui
 ============================================================
 [*] Now Starting Connect6 Scrape:
 [*] SimplyEmail has attempted to find correct URL for Connect6:
     URL detected: www.connect6.com/Vfffffff,%20LLC/c 
 [>] Is this URL correct?: n
    Potential URL: www.connect6.com/Vffffffff,%20LLC/c 
    Potential URL: www.connect6.com/fffffff/p/181016043240247014147078237069133079124017210127108009097255039209172025193089206212192166241042174198072085028234035215132077249038065254013074 
    Potential URL: www.connect6.com/Cfffff/p/034097047081090085111147210185030172009078049169022098212236211095220195001177030045187199131226210223245205084079141193247011181189036140240023 
    Potential URL: www.connect6.com/Jfffffff/p/102092136035048036136024218227078226242230121102078233031208236153124239181008089103120004217018 
    Potential URL: www.connect6.com/Adam-Salerno/p/021252074213080142144144173151186084054192089124012168233122054057047043085086050013217026242085213002224084036030244077024184140161144046156080 
 [!] GoogleDork This: site:connect6.com "Vfffff.com"
 [-] Commands Supported: (B) ack - (R) etry
 [>] Please Provid a URL: b

```

## Verifying Emails via target SMTP server:
More often than not you will have at least a few invalid emails gathered from recon. SimplyEmail now supports
the ability to verify and check if the email is valid.
- Looks up MX records
- Sorts based on priority 
- Checks if SMTP server will respond other than 250
- If the server is suitable, checks for 250 codes
- Outputs a (.txt) file with verified emails. 

```
============================================================
 Curent Version: v1.0 | Website: CyberSyndicates.com
 ============================================================
 Twitter: @real_slacker007 |  Twitter: @Killswitch_gui
 ============================================================
 [*] Email reconnaissance has been completed:

    Email verification will allow you to use common methods
    to attempt to enumerate if the email is valid.
    This grabs the MX records, sorts and attempts to check
    if the SMTP server sends a code other than 250 for known bad addresses

 [>] Would you like to verify email(s)?: y
 [*] Attempting to resolve MX records!
 [*] MX Host: gmail-smtp-in.l.google.com.
 [*] Checking for valid email: alwathiqlegaltranslation@gmail.com
 [!] Email seems valid: alwathiqlegaltranslation@gmail.co
```

## Understanding Reporting Options:
One of the most frustrating aspects of Pen-testing is the tools' ability
to report the findings and make those easily readable. This may be for the data
provided to a customer or just the ability to report on source of the data.

So I'm making it my goal for my tools to take that work off your back and make it as simple as possible!
Let's cover the two different reports generated.
### Text Output:
With this option results are generated and appended to a running text file called Email_List.txt. 
this makes it easy to find past searches or export to tool of choice. Example:
```
  ----------------------------------
  Email Recon: 11/11/2015 05:13:32
  ----------------------------------
bo@mandiant.com
in@mandiant.com
sc@mandiant.com
je@mandiant.com
su@mandiant.com
----------------------------------
  Email Recon: 11/11/2015 05:15:42
  ----------------------------------
bo@mandiant.com
in@mandiant.com
sc@mandiant.com
je@mandiant.com
su@mandiant.com
```
### JSON Output
using the ```--json test.txt``` flag will alow you to output standard JSON text file for automation needs. This can be currently used with the email scraping portion only, maybe name generation and email verification to come. These helpers will be soon in the SQL DB and API for more streamline automation. Example output:
```
{
    "current_version": "v1.4.1", 
    "data_of_collection": "26/06/2016", 
    "domain_of_collection": "---SNIP---", 
    "email_collection_count": 220, 
    "emails": [
        {
            "collection_data": "26/06/2016", 
            "collection_time": "18:47:42", 
            "email": "---SNIP---", 
            "module_name": "Searching PGP"
        }, 
       ---SNIP---
        {
            "collection_data": "26/06/2016", 
            "collection_time": "18:51:46", 
            "email": "---SNIP---", 
            "module_name": "Exalead PDF Search for Emails"
        }
    ], 
    "time_of_collection": "18:53:04", 
    "tool_of_collection": "SimplyEmail"
}
```
### HTML Output:
As I mentioned before a powerful function that I wanted to integrate was the ability to produce a visually appealing and rich report for the user and potentially something that could be part of data provided to a client. Please let me know with suggestions! 
#### Email Source:
![Alt text](/bootstrap-3.3.5/Screen Shot 2015-11-11 at 5.27.15 PM.png?raw=true "Report")
#### Email Section:
- Html report now shows Alerts for Canary Search Results!
![Alt text](/bootstrap-3.3.5/Screen Shot 2015-11-11 at 5.27.31 PM.png?raw=true "Report Html")

#### TODO:
```
Modules Under Dev:
-----------------------------
( ) StartPage Search (can help with captcha issues)
( ) Searching SEC Data
( ) PwnBin Search 
( ) Past Data Dumps
( ) psbdmp API Based and non Alert

Framework Under Dev:
-----------------------------
( ) New Parsers to clean results
( ) Fix import errors with Glob
( ) Add in "[@]something.com" to search Regex and engines
( ) Add Threading/Multi to GitHub Search
( ) Add Source of collection to HTML Output

Current Issues:
-----------------------------
( ) PDF miner Text Extraction Error
( ) Verify Emails function and only one name list raises errors

```

