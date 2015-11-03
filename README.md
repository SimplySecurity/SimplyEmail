# SimplyEmail

What is the simple email recon tool? This tool was based off the work of theHarvester and kind of a port of the functionality. This was just an expansion of what was used to build theHarvester and will incorporate his work but allow users to easily build Modules for the Framework. Which I felt was desperately needed after building my first module for theHarvester.

A few small benfits:
- Easy for you to write modules (All you need is 3 required Class options and your up and running)
- Multiprocessing Queue for modules and Result Queue for easy handling of Email data 
- Simple intergration of theHarvester Modules and new ones to come
- Also the ability to change major settings fast without diving into the code
 
##Build Log:
####Changelog in 0.1:
```
Modules Added in v0.1:
-----------------------------
(x) HtmlScrape Added to Modules 
(x) SearchPGP Added to Modules - Port form theHarvester
(x) Google Search - Port form theHarvester
(x) Flickr Page Search
(x) GitHub Code Search

Issues Fixed in v0.1:
-----------------------------
(x) Wget fails to follow redirects in some cases

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
( ) Searching SEC Data
( ) PDFMiner 
( ) Exalead Search - Port from theHarvester
( ) GitHubGist 
( ) PasteBin Searches 
( ) Past Data Dumps
( ) Canary API based and non API

Framework Under Dev:
-----------------------------
( ) New Parsers to clean results
( ) Fix import errors with Glob
( ) Add in "[@]something.com" to search Regex and engines
( ) Add errors for Captcha limit's
(/) Add auto redirects for WGET and supplied Domain Names: may need httrack?
( ) Add Threading/Multi to GitHub Search
( ) Fix Issues with Join()
```


## Standard Help
```
 ============================================================
 Curent Version: 0.1 | Website: Cyber-Syndicates.com
 ============================================================
 Twitter: @real_slacker007 |  Twitter: @Killswitch_gui
 ============================================================
------------------------------------------------------------------------------
   ______  ________                       __ __ 
 /      \/        |                     /  /  |
/$$$$$$  $$$$$$$$/ _____  ____   ______ $$/$$ |
$$ \__$$/$$ |__   /     \/    \ /      \/  $$ |
$$      \$$    |  $$$$$$ $$$$  |$$$$$$  $$ $$ |
 $$$$$$  $$$$$/   $$ | $$ | $$ |/     $$ $$ $$ |
/  \__$$ $$ |_____$$ | $$ | $$ /$$$$$$$ $$ $$ |
$$    $$/$$       $$ | $$ | $$ $$    $$ $$ $$ |
 $$$$$$/ $$$$$$$$/$$/  $$/  $$/ $$$$$$$/$$/$$/

------------------------------------------------------------------------------
usage: SimplyEmail.py [-all] [-e company.com] [-l]

Email enumeration is an important phase of so many operation that a pen-tester
or Red Teamer goes through. There are tons of applications that do this but I
wanted a simple yet effective way to get what Recon-Ng gets and theHarvester
gets. (You may want to run -h)

optional arguments:
  -all            Use all non API methods to obtain Emails
  -e company.com  Set required email addr user, ex ale@email.com
  -l              List the current Modules Loaded


```

## Run SimpleEmail

Lets say your target is cybersyndicates.com
```python
./SimplyEmail.py -all -e cybersyndicates.com
```
This will run ALL modules that are have API placed in the SimpleEmail.ini file and will run all non-API based modules. 
## List Modules SimpleEmail
```
root@vapt-kali:~/Desktop/SimplyEmail# ./SimplyEmail.py -l

 ============================================================
 Curent Version: 0.1 | Website: Cyber-Syndicates.com
 ============================================================
 Twitter: @real_slacker007 |  Twitter: @Killswitch_gui
 ============================================================
------------------------------------------------------------------------------
   ______  ________                       __ __ 
 /      \/        |                     /  /  |
/$$$$$$  $$$$$$$$/ _____  ____   ______ $$/$$ |
$$ \__$$/$$ |__   /     \/    \ /      \/  $$ |
$$      \$$    |  $$$$$$ $$$$  |$$$$$$  $$ $$ |
 $$$$$$  $$$$$/   $$ | $$ | $$ |/     $$ $$ $$ |
/  \__$$ $$ |_____$$ | $$ | $$ /$$$$$$$ $$ $$ |
$$    $$/$$       $$ | $$ | $$ $$    $$ $$ $$ |
 $$$$$$/ $$$$$$$$/$$/  $$/  $$/ $$$$$$$/$$/$$/

------------------------------------------------------------------------------
 [*] Available Modules are:

	1)	Modules/HtmlScrape.py   
	2)	Modules/SearchPGP.py    
	3)	Modules/PDFMiner.py  
```
