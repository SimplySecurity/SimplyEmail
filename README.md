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
- Easy for you to write modules (All you need is 1 required Class options and your up and running)
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
 Curent Version: 0.1 | Website: CyberSyndicates.com
 ============================================================
 Twitter: @real_slacker007 |  Twitter: @Killswitch_gui
 ============================================================
-----------------------------------------------------------------------------
   ______  ________                       __ __ 
 /      \/        |                     /  /  |
/$$$$$$  $$$$$$$$/ _____  ____   ______ $$/$$ |
$$ \__$$/$$ |__   /     \/    \ /      \/  $$ |
$$      \$$    |  $$$$$$ $$$$  |$$$$$$  $$ $$ |
 $$$$$$  $$$$$/   $$ | $$ | $$ |/     $$ $$ $$ |
/  \__$$ $$ |_____$$ | $$ | $$ /$$$$$$$ $$ $$ |
$$    $$/$$       $$ | $$ | $$ $$    $$ $$ $$ |
 $$$$$$/ $$$$$$$$/$$/  $$/  $$/ $$$$$$$/$$/$$/

-----------------------------------------------------------------------------
usage: SimplyEmail.py [-all] [-e company.com] [-s] [-l]
                      [-t html / flickr / google]

Email enumeration is a important phase of so many operation that a pen-tester
or Red Teamer goes through. There are tons of applications that do this but I
wanted a simple yet effective way to get what Recon-Ng gets and theHarvester
gets. (You may want to run -h)

optional arguments:
  -all                  Use all non API methods to obtain Emails
  -e company.com        Set required email addr user, ex ale@email.com
  -s                    Show only emils matching your domain (We may want to
                        collect all emails for potential connections)
  -l                    List the current Modules Loaded
  -t Html / Flickr / Google
                        Test individual module (For Linting)
```

### Run SimplyEmail

Lets say your target is cybersyndicates.com
```python
./SimplyEmail.py -all -e cybersyndicates.com
```
This will run ALL modules that are have API Key placed in the SimpleEmail.ini file and will run all non-API based modules. 
### List Modules SimpleEmail
```
root@vapt-kali:~/Desktop/SimplyEmail# ./SimplyEmail.py -l

 ============================================================
 Curent Version: 0.1 | Website: CyberSyndicates.com
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
	6)	Modules/EmailHunter.py  
	7)	Modules/WhoisAPISearch.py
	8)	Modules/SearchPGP.py    
	9)	Modules/GoogleSearch.py 
	10)	Modules/GitHubGistSearch.py
	11)	Modules/FlickrSearch.py 
```
##Build Log:
####Changelog in of v0.2:
```
Modules Added in v0.2:
-----------------------------
(x) EmailHunter Trial API

Issues Fixed in v0.2:
-----------------------------
(x) Fixed Issues with SetupScript 
(x) Changes Output Text file name

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
