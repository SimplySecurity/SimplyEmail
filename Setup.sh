#!/bin/bash

# Global Variables
runuser=$(whoami)
tempdir=$(pwd)

# Title Function
func_title(){
  # Clear (For Prettyness)
  clear

  # Echo Title
  echo '=========================================================================='
  echo ' SimpleEmail Setup Script | [Updated]: 2016'
  echo '=========================================================================='
  echo ' [Web]: Http://CyberSyndicates.com | [Twitter]: @KillSwitch-GUI'
  echo '=========================================================================='
}



# Environment Checks
func_check_env(){
  # Check Sudo Dependency going to need that!
  if [ $(which sudo|wc -l) -eq '0' ]; then
    echo
    echo ' [ERROR]: This Setup Script Requires sudo!'
    echo '          Please Install sudo Then Run This Setup Again.'
    echo
    exit 1
  fi
}

func_install_requests(){
  echo ' [*] Installing and updating requests libary'
  #Insure we have the latest requests module in python
  #sudo apt-get -q update
  #sudo apt-get -q upgrade 
  sudo git pull
  # remove bad pcks (Kali Python 2016.1 rolling issues)
  sudo apt-get remove python-configparser
  sudo apt-get remove python-magic
  # setup PPTX depends 
  sudo apt-get -y install python-lxml
  sudo apt-get -y install wget grep antiword odt2txt python-dev libxml2-dev libxslt1-dev
  chmod 755 SimplyEmail.py
  sudo pip install --upgrade xlsxwriter
  sudo pip install beautifulsoup4
  sudo pip install python-magic
  sudo pip install fake-useragent --upgrade
  sudo pip install mechanize --upgrade
  sudo pip install docx2txt --upgrade
  sudo pip install requests --upgrade
  sudo pip install xlsx2csv --upgrade
  sudo pip install configparser --upgrade
  sudo pip install BeautifulSoup --upgrade
  sudo pip install pdfminer --upgrade
  sudo pip install dnspython --upgrade

}


# Menu Case Statement
case $1 in
  *)
  func_title
  func_check_env
  func_install_requests
  ;;

esac
