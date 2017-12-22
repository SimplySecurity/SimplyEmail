func_check_env(){
  # Check Sudo Dependency going to need that!
  if [[ "$OSTYPE" == "darwin"* ]]; then
    # MacOS / OS X
    xcode-select --install
    /usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
    brew install curl
    brew install git  
  fi

  if [ -f /etc/debian_version ]; then
    sudo apt install -y git
    sudo apt install -y curl
    sudo apt install -y sudo
  fi
  
  if [ -f /etc/redhat-release ]; then
    sudo dnf install -y git
    sudo dnf install -y curl
    sudo dnf install -y sudo
  fi

  if [ -f /etc/lsb-release ]; then
    sudo apt-get -y install git
    sudo apt-get -y install curl
    sudo apt-get -y install sudo
  fi
  
  if [ $(which sudo|wc -l) -eq '0' ]; then
    echo
    echo ' [ERROR]: This Setup Script Requires sudo!'
    echo '          Please Install sudo Then Run This Setup Again.'
    echo
    exit 1
  fi
  
  git clone --branch master https://github.com/killswitch-GUI/SimplyEmail.git
  cd SimplyEmail
  ./setup/setup.sh
}


case $1 in
  *)
  func_check_env
  ;;

esac
