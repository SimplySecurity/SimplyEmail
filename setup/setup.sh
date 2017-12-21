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
  sudo git pull
  if [ -f /etc/redhat-release ]; then
    sudo dnf install -y python-lxml
    sudo dnf install -y wget grep antiword odt2txt python-devel libxml2-devel libxslt1-devel
  fi

  if [ -f /etc/lsb-release ]; then
    sudo apt-get -y install python-lxml
  	sudo apt-get -y install wget grep antiword odt2txt python-dev libxml2-dev libxslt1-dev
  fi
  # Check for PIP otherwise install it
  if ! which pip > /dev/null; then
    wget https://bootstrap.pypa.io/get-pip.py
    python get-pip.py
  fi
}

func_install_env(){
  if [ -f /.dockerenv ]; then
      echo " [*] Currently installing to Docker, skipping Python Virtenv"
  else
    # Setup virtual env
    pip install autoenv
    echo "source `which activate.sh`" >> ~/.bashrc
    apt-get install python-virtualenv -y
    virtualenv --no-site-packages SE
    source SE/bin/activate
  fi 
}

func_install_pip(){
   pip install -r setup/requirments.txt 
}

# Menu Case Statement
case $1 in
  *)
  func_title
  func_check_env
  func_install_requests
  func_install_env
  func_install_pip
  ;;

esac

