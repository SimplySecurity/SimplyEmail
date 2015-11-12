[![Build Status](https://travis-ci.org/killswitch-GUI/SimplyEmail.svg?branch=master)](https://travis-ci.org/killswitch-GUI/SimplyEmail)
# SimplyEmail

What is the simple email recon tool? This tool was based off the work of theHarvester and kind of a port of the functionality. This was just an expansion of what was used to build theHarvester and will incorporate his work but allow users to easily build Modules for the Framework. Which I felt was desperately needed after building my first module for theHarvester.

MAJOR CALLOUTS:
@laramies - Devloper of theHarvester tool https://github.com/laramies/theHarvester

Work Conducted by:
----------------------------------------------
* Alexander Rymdeko-Harvey [Twitter] @Killswitch-GUI -- [Web] [CyberSydicates.com](http://cybersyndicates.com)
* Keelyn Roberts [Twitter] @real_slacker007 -- [Web] [CyberSydicates.com](http://cybersyndicates.com)

## Scrape EVERYTHING - Simply 

A few small benfits:
- Easy for you to write modules (All you need is 1 required Class option and your up and running)
- Use the built in Parsers for most raw results
- Multiprocessing Queue for modules and Result Queue for easy handling of Email data 
- Simple intergration of theHarvester Modules and new ones to come
- Also the ability to change major settings fast without diving into the code

API Based Searches:
- When API based searches become avaliable, no need to add them to the Command line
- API keys will be auto pulled from the SimpleEmail.ini, this will activate the module for use
 
## Get Started
Please RUN the simple Setup Bash script!!!
```Bash
root@kali:~/Desktop/SimplyEmail# sh Setup.sh
or
root@kali:~/Desktop/SimplyEmail# ./Setup.sh
```

### Standard Help
```
 ============================================================
 Curent Version: 0.4 | Website: CyberSyndicates.com
 ============================================================
 Twitter: @real_slacker007 |  Twitter: @Killswitch_gui
 ============================================================
------------------------------------------------------------
   ______  ________                       __ __
 /      \/        |                     /  /  |
/$$$$$$  $$$$$$$$/ _____  ____   ______ $$/$$ |
$$ \__$$/$$ |__   /     \/    \ /      \/  $$ |
$$      \$$    |  $$$$$$ $$$$  |$$$$$$  $$ $$ |
 $$$$$$  $$$$$/   $$ | $$ | $$ |/     $$ $$ $$ |
/  \__$$ $$ |_____$$ | $$ | $$ /$$$$$$$ $$ $$ |
$$    $$/$$       $$ | $$ | $$ $$    $$ $$ $$ |
 $$$$$$/ $$$$$$$$/$$/  $$/  $$/ $$$$$$$/$$/$$/

------------------------------------------------------------
usage: SimplyEmail.py [-all] [-e company.com] [-l] [-t html / flickr / google]
                      [-v]

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
  -v                    Set this switch for verbose output of modules

```

### Run SimplyEmail

Lets say your target is cybersyndicates.com
```python
./SimplyEmail.py -all -e cybersyndicates.com
or in verbose
./SimplyEmail.py -all -v -e cybersyndicates.com
```
This will run ALL modules that are have API Key placed in the SimpleEmail.ini file and will run all non-API based modules. 

### List Modules SimpleEmail
```
root@vapt-kali:~/Desktop/SimplyEmail# ./SimplyEmail.py -l

 ============================================================
 Curent Version: 0.4 | Website: CyberSyndicates.com
 ============================================================
 Twitter: @real_slacker007 |  Twitter: @Killswitch_gui
 ============================================================
------------------------------------------------------------
   ______  ________                       __ __
 /      \/        |                     /  /  |
/$$$$$$  $$$$$$$$/ _____  ____   ______ $$/$$ |
$$ \__$$/$$ |__   /     \/    \ /      \/  $$ |
$$      \$$    |  $$$$$$ $$$$  |$$$$$$  $$ $$ |
 $$$$$$  $$$$$/   $$ | $$ | $$ |/     $$ $$ $$ |
/  \__$$ $$ |_____$$ | $$ | $$ /$$$$$$$ $$ $$ |
$$    $$/$$       $$ | $$ | $$ $$    $$ $$ $$ |
 $$$$$$/ $$$$$$$$/$$/  $$/  $$/ $$$$$$$/$$/$$/

------------------------------------------------------------
 [*] Available Modules are:

	1)	Modules/HtmlScrape.py   
	2)	Modules/Whoisolgy.py    
	3)	Modules/CanaryBinSearch.py
	4)	Modules/YahooSearch.py  
	5)	Modules/GitHubCodeSearch.py
	6)	Modules/AskSearch.py    
	7)	Modules/EmailHunter.py  
	8)	Modules/WhoisAPISearch.py
	9)	Modules/SearchPGP.py    
	10)	Modules/GoogleSearch.py 
	11)	Modules/GitHubGistSearch.py
	12)	Modules/OnionStagram.py 
	13)	Modules/FlickrSearch.py 
```
## Understanding Reporting Options:
One of the most frustrating aspects of Pen-testing is the tools ability
to report the findings and make those easily readable. This may be for the data
provided to a customer or just the ability to report on source of the data.

So I’m making it my goal for my tools to take that work off your back and make it as simple as possible!
Let’s cover the two different reports generated.
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
### HTML Output:
As I mentioned before a powerful function that I wanted to integrate was the ability to produce a visually appealing and rich report for the user and potentially something that could be part of data provided to a client. Please let me know with suggestions! 
#### Email Source:
![Alt text](/bootstrap-3.3.5/Screen Shot 2015-11-11 at 5.27.15 PM.png?raw=true "Report")
#### Email Section:
![Alt text](/bootstrap-3.3.5/Screen Shot 2015-11-11 at 5.27.31 PM.png?raw=true "Report Html")
##Current Email Evasion Techniques
- The following will be built into the Parser Soon:
- shinichiro.hamaji _at_ gmail.com
- shinichiro.hamaji _AT_ gmail.com
- simohayha.bobo at gmail.com
- "jeffreytgilbert" => "gmail.com"
- felix021 # gmail.com
- hirokidaichi[at]gmail.com
- hirokidaichi[@]gmail.com 
- hirokidaichi[#]gmail.com
- xaicron{ at }gmail.com
- xaicron{at}gmail.com
- xaicron{@}gmail.com
- xaicron(@)gmail.com
- xaicron + gmail.com
- xaicron ++ gmail.com
- xaicron ## gmail.com
- bekt17[@]gmail.com
- billy3321 -AT- gmail.com
- billy3321[AT]gmail.com
- ybenjo.repose [[[at]]] gmail.com
- sudhindra.r.rao (at) gmail.com
- sudhindra.r.rao nospam gmail.com
- shinichiro.hamaji (.) gmail.com
- shinichiro.hamaji--at--gmail.com

##Build Log:
####Changelog (Current v0.4):
```
===================================
Modules Added in v0.4
-----------------------------
(x) GitHubUser added

Issues Fixed in v0.4:
-----------------------------
(x) Setup File Fix

Framework Improvements v0.4:
-----------------------------
(x) Added Source of email collection
	to final report in bootstrap.
(x) Added Verbose options for Modules
	to handle Vebose printing.

===================================
Modules Added in v0.3:
-----------------------------
(x) OnionStagram (Instagram User Search)
(x) AskSearch - Port from theHarvester

Issues Fixed in v0.3:
----------------------------
(x) Added Parser to GitHubCode Search
(x) Moved wget to 2 sec timeout

===================================
Modules Added in v0.2:
-----------------------------
(x) EmailHunter Trial API

Issues Fixed in v0.2:
-----------------------------
(x) Fixed Issues with SetupScript 
(x) Changes Output Text file name

===================================
Modules Added in v0.1:
-----------------------------
(x) HtmlScrape Added to Modules 
(x) SearchPGP Added to Modules - Port form theHarvester
(x) Google Search - Port form theHarvester
(x) Flickr Page Search
(x) GitHub Code Search
(x) GitHubGist Code Search
(x) Whois Non-Auth API Search
(x) Whoisology Search
(x) Yahoo Search - Port from theHarvester
(x) Canary (Non-API) PasteBin Search for Past Data Dumps!

Issues Fixed in v0.1:
-----------------------------
(x) Wget fails to follow redirects in some cases
(x) Fixed Issues with google search
(x) Major change with how the Framework Handles Consumer and Producred Model
(x) Fix Issues with Join() and Conducter

Imprrovements in v0.1:
-----------------------------
(x) Added in valid UserAgents and headers
(x) HTML Scrape now has opption to save or remove is mirror
(x) HTML Scrape UTF-8 issues fixed
```
####Build out Path:
```
Modules Under Dev:
-----------------------------
( ) StartPage Search (can help with captcha issues)
( ) GitHub User Search
( ) Searching SEC Data
( ) PDFMiner 
( ) Exalead Search - Port from theHarvester
( ) PwnBin Search 
( ) PasteBin Searches 
( ) Past Data Dumps
( ) Canary API based and non API
( ) psbdmp API Based and non Alert

Framework Under Dev:
-----------------------------
( ) New Parsers to clean results
( ) Fix import errors with Glob
( ) Add in "[@]something.com" to search Regex and engines
( ) Add errors for Captcha limit's
( ) Add Threading/Multi to GitHub Search
( ) Add Source of collection to HTML Output

```
