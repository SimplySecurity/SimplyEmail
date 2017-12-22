func_check_env(){
  # Check Sudo Dependency going to need that!
  if [ $(which sudo|wc -l) -eq '0' ]; then
    echo
    echo ' [ERROR]: This Setup Script Requires sudo!'
    echo '          Please Install sudo Then Run This Setup Again.'
    echo
    exit 1
  fi
  if [ -f /etc/debian_version ]; then
    sudo apt install git
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
