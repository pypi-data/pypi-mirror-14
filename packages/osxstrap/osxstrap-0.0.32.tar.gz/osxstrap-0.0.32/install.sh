#!/bin/bash

# Colors
GREEN='\e[1;32m'
RED='\e[1;31m'
BLUE='\e[1;34m'
PURPLE='\e[1;35m'
YELLOW='\e[1;33m'
CYAN='\e[1;36m'
GRAY='\e[1;37m'
DARK_GRAY='\e[1;30m'
WHITE='\e[1;37m'
COLOR_OFF='\e[0m'

# Command line arg defaults
REPO_URL="https://github.com/osxstrap/osxstrap"
VERBOSE=0
INSTALL_DIR="$HOME/Library/Application Support/osxstrap"
INSTALL_DIR_DEFAULT=$INSTALL_DIR
DEV_INSTALL=0
CONFIG_FILE_PATH=""
ORIGINAL_PWD=$PWD
OPTS="vhi:r:c:"

function output_running {
	printf "${PURPLE}--> ${COLOR_OFF}$1\n" 1>&2
}

function output_success {
	printf "${GREEN}++ OK: ${COLOR_OFF}$1\n" 1>&2
}

function output_skip {
	printf "${GREEN}-- SKIPPED: ${COLOR_OFF}$1\n" 1>&2
}

function output_header {
	printf "\n${WHITE}[[ ${COLOR_OFF}$1${WHITE} ]]${COLOR_OFF}\n\n" 1>&2
}

function output_debug {
	if [ "$VERBOSE" = 1 ] ; then
		printf "${DARK_GRAY}| DEBUG: ${COLOR_OFF}$1\n" 1>&2
	fi
}

function output_warning {
	printf "${YELLOW}! WARNING: ${COLOR_OFF}$1\n" 1>&2
}

function error {
	printf "\n${RED}!! ERROR: ${COLOR_OFF}$1\n\nExiting.\n" 1>&2
	exit 1
}
  
function banner {
printf "${PURPLE}                         _                      ${COLOR_OFF}\n"
printf "${PURPLE}                        | |                     ${COLOR_OFF}\n"
printf "${PURPLE}   ___   ___ __  __ ___ | |_  _ __  __ _  _ __  ${COLOR_OFF}\n"
printf "${PURPLE}  / _ \ / __|\ \/ // __|| __|| '__|/ _\` || '_ \ ${COLOR_OFF}\n"
printf "${PURPLE} | (_) |\__ \ >  < \__ \| |_ | |  | (_| || |_) |${COLOR_OFF}\n"
printf "${PURPLE}  \___/ |___//_/\_\|___/ \__||_|   \__,_|| .__/ ${COLOR_OFF}\n"
printf "${PURPLE}                                         | |    ${COLOR_OFF}\n"
printf "${PURPLE}                                         |_|    ${COLOR_OFF}\n"
printf "${PURPLE}                             http://osxstrap.org${COLOR_OFF}\n\n"
printf "${DARK_GRAY}Thanks:${COLOR_OFF}\n${BLUE}http://superlumic.com\nhttps://github.com/boxcutter/osx\nhttp://patorjk.com/software/taag\nhttps://gist.github.com/pkuczynski/8665367${COLOR_OFF}\n\n"
}

# Check whether a command exists - returns 0 if it does, 1 if it does not
function exists {
  output_debug "Checking if the '$1' command is present."
  if command -v $1 >/dev/null 2>&1
  then
	output_debug "Command '$1' is present."
	return 0
  else
	output_debug "Command '$1' is not present."
	return 1
  fi
}

function fail_on_error {
  if ! $1
  then error "Command '$1' returned a non zero exit code."
  fi
}

function warn_on_error {
  if ! $1
  then output_warning "Command '$1' returned a non zero exit code."
  fi
}

usage()
{
cat << EOF

usage: $0 options

OPTIONS:
   -h      Show this message.
   -v      Enable verbose output.
   -c      Config file path.
   -i      Install directory path. Default: $INSTALL_DIR
   -r      Git repo URL to install osxstrap from. Default: $REPO_URL
EOF
}

# credits https://github.com/boxcutter/osx/blob/master/script/xcode-cli-tools.sh
function install_clt {
	output_header "Installing Command Line Tools"

	if [[ -f "/Library/Developer/CommandLineTools/usr/bin/clang" ]]; then
		output_skip "Command Line Tools already installed."
		return 0
	fi

	# Get and install Xcode CLI tools
	OSX_VERS=$(sw_vers -productVersion | awk -F "." '{print $2}')

	# on 10.9+, we can leverage SUS to get the latest CLI tools
	if [ "$OSX_VERS" -ge 9 ]; then
		# create the placeholder file that's checked by CLI updates' .dist code
		# in Apple's SUS catalog
		touch /tmp/.com.apple.dt.CommandLineTools.installondemand.in-progress
		# find the CLI Tools update
		PROD=$(softwareupdate -l | grep "\*.*Command Line" | head -n 1 | awk -F"*" '{print $2}' | sed -e 's/^ *//' | tr -d '\n')
		# install it
		softwareupdate -i "$PROD" -v
		rm /tmp/.com.apple.dt.CommandLineTools.installondemand.in-progress

	# on 10.7/10.8, we instead download from public download URLs, which can be found in
	# the dvtdownloadableindex:
	# https://devimages.apple.com.edgekey.net/downloads/xcode/simulators/index-3905972D-B609-49CE-8D06-51ADC78E07BC.dvtdownloadableindex
	else
		[ "$OSX_VERS" -eq 7 ] && DMGURL=http://devimages.apple.com.edgekey.net/downloads/xcode/command_line_tools_for_xcode_os_x_lion_april_2013.dmg
		[ "$OSX_VERS" -eq 7 ] && ALLOW_UNTRUSTED=-allowUntrusted
		[ "$OSX_VERS" -eq 8 ] && DMGURL=http://devimages.apple.com.edgekey.net/downloads/xcode/command_line_tools_for_osx_mountain_lion_april_2014.dmg

		TOOLS=clitools.dmg
		curl "$DMGURL" -o "$TOOLS"
		TMPMOUNT=`/usr/bin/mktemp -d /tmp/clitools.XXXX`
		hdiutil attach "$TOOLS" -mountpoint "$TMPMOUNT"
		installer $ALLOW_UNTRUSTED -pkg "$(find $TMPMOUNT -name '*.mpkg')" -target /
		hdiutil detach "$TMPMOUNT"
		rm -rf "$TMPMOUNT"
		rm "$TOOLS"
	fi

	if [[ ! -f "/Library/Developer/CommandLineTools/usr/bin/clang" ]]; then
		error "Command Line Tools installation failed. Exiting."
	else
		output_success "Command Line Tools successfully installed."
	fi
}

function install_pip {
	output_header "Installing pip"
	if ! exists pip; then
		fail_on_error "sudo easy_install --quiet pip"
		if ! exists pip; then
			error "Error installing pip."
		else
			output_success "pip successfully installed."
		fi
	else
		output_skip "pip already installed."
	fi
}

function install_ansible {
	output_header "Installing Ansible"
	if ! exists ansible; then
		fail_on_error "sudo pip install -I ansible==1.9.4"
		if ! exists ansible; then
			error "Error installing Ansible."
		else
			output_success "Ansible successfully installed."
		fi
	else
		output_skip "Ansible already installed."
	fi
}

function install_osxstrap {
	output_header "Installing/Updating osxstrap"
	output_running "Creating install directory '$INSTALL_DIR'."
	if [ "$DEV_INSTALL" = 0 ]; then
		mkdir -p "$INSTALL_DIR"
		if [ -d "$INSTALL_DIR/.git" ]; then
			output_running "Updating osxstrap core using git"
			cd "$INSTALL_DIR"
			warn_on_error "git pull -q"
		else
			output_running "Cloning osxstrap core from $REPO_URL"
			cd "$INSTALL_DIR"
			fail_on_error "git clone -q $REPO_URL ."
		fi
	else
		output_skip "Dev install"
	fi
}

function install_osxstrap_command {
	output_header "Installing osxstrap command"
	if [ "$DEV_INSTALL" = 0 ]; then
		if ! exists osxstrap; then
			fail_on_error "sudo pip install osxstrap"
		else
			output_skip "osxstrap command already installed, checking for updates."
			fail_on_error "sudo pip install osxstrap -U"
		fi
	else
		fail_on_error "sudo pip install -e ."
	fi
}

function init_osxstrap {
	output_header "Running osxstrap init"
	cd "$ORIGINAL_PWD"
	fail_on_error "osxstrap init -c $CONFIG_FILE_PATH"
}

banner

while getopts "$OPTS" OPTION
do
	case $OPTION in
		h)
			usage
			exit 1
			;;
		v)
			VERBOSE=1
			;;
		i)
			INSTALL_DIR=$OPTARG
			;;
		r)
			REPO_URL=$OPTARG
			;;
		c)
			CONFIG_FILE_PATH=$OPTARG
			;;
		?)
			usage
			exit
			;;
	esac
done

shell="$1"
if [ -z "$shell" ]; then
	shell="$(basename "$SHELL")"
fi

if [ -d "$ORIGINAL_PWD/.git" ]; then
	if [ -f "$ORIGINAL_PWD/osxstrap" ]; then
		output_debug "Current directory is git repo containing osxstrap script, using it as INSTALL_DIR"
		INSTALL_DIR=$ORIGINAL_PWD
		DEV_INSTALL=1
	fi
fi

if [ "$VERBOSE" = 1 ] ; then
	output_debug "Detected verbose (-v) flag."
fi

output_debug "Install directory is '$INSTALL_DIR'."

output_debug "Git repo URL is '$REPO_URL'."

output_debug "Checking if we need to ask for a sudo password"

sudo -v

output_debug "Keep-alive: update existing sudo time stamp until we are finished"

while true; do sudo -n true; sleep 60; kill -0 "$$" || exit; done 2>/dev/null &

install_clt

install_pip

install_ansible

install_osxstrap

install_osxstrap_command

init_osxstrap