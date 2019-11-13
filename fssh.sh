#!/usr/bin/env bash
set -o errexit
set -o pipefail
set -o noclobber

__dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" >/dev/null 2>&1 && pwd)"
__file="${__dir}/$(basename "${BASH_SOURCE[0]}")"
__base="$(basename ${__file} .sh)"

grant() {
  # https://api.github.com/users/runarsf/keys # not hub/lab standardized
  # https://github.com/runarsf.keys
  # https://gitlab.com/runarsf.keys
  #if [ "$(command -v curl >/dev/null 2>&1)" ]; then
  if [ "$(command -v curl)" ]; then
    (set "${verbosity}"; \cp -f "${HOME}"/.ssh/authorized_keys "${HOME}"/.ssh/authorized_keys.bak)
    (set "${verbosity}"; curl --silent --show-error https://"${host}"/"${user}".keys >> "${HOME}"/.ssh/authorized_keys)
  elif [ "$(command -v wget)" ]; then
    (set "${verbosity}"; \cp -f "${HOME}"/.ssh/authorized_keys "${HOME}"/.ssh/authorized_keys.bak)
    (set "${verbosity}"; wget --quiet --no-verbose https://"${host}"/"${user}".keys -O ->> "${HOME}"/.ssh/authorized_keys)
  else
    echo "This script needs either curl or wget to run, but neither of them seem to be installed."
    exit 1
  fi

	cat <<-EOMAN
	Added key(s) to ~/.ssh/authorized_keys
	Press ^C to terminate the script and revert all changes.
	Your friend can now access this computer with:

	 - Local: ssh $(whoami)@$(hostname -I | cut -d' ' -f1)
	 - External: ssh $(whoami)@$(dig @resolver1.opendns.com ANY myip.opendns.com +short)
	EOMAN
  sleep "${timeout}"
  revoke
  exit 0
}

revoke() {
  (set "${verbosity}"; mv -f "${HOME}"/.ssh/authorized_keys.bak "${HOME}"/.ssh/authorized_keys)
}
trap "revoke; exit 0" INT

prompt() {
  printf "${1} [y/N]"
  read -p " " -n 1 -r </dev/tty
  printf "\n"
  if [[ ! "${REPLY}" =~ ^[Yy]$ ]]; then
    return 1
  fi
}

helpme() {
	cat <<-EOMAN
	Usage: fssh [options] [commands]

	Options:
	  -h, --help                  Display this message.
	  -l, --gitlab                Look for key on GitLab instead of GitHub.
	  -t, --timeout <ms>          Time before script is automatically terminated. (s, m, h, d)
	  -y, --noconfirm             Disable confirmation dialog.
	  -v, --verbose               Enable verbose mode.
	  -i, --install <method>      Install the script, 'hard' for permanent, 'link' to symlink. User will be prompted for sudo rights.
	  -u, --uninstall             Uninstall the script. Requires user confirmation.
	  -r, --revert                Revert changes made by the script.

	Commands:
	  <username>                  The username of the trusted individual.

	Examples:
	  pkill -f fssh               Terminates all running script instances, run with --revert after termination.
	  fssh runarsf &              Start script in background, but preserve output.
	  fssh runarsf
	  fssh --gitlab runarsf
	  fssh --timeout 30m runarsf
	  fssh --noconfirm runarsf
	  fssh --verbose runarsf
	  fssh --install hard
	  fssh --uninstall
	  fssh --rever
	EOMAN
}

# If there is no argument, display help menu
test "${#}" -lt "1" \
  && helpme \
  && exit 0
timeout='infinity' host='github.com' user='' noconfirm='false' verbosity='+x'
POSITIONAL=()
while [[ $# -gt 0 ]]; do
  case "${1}" in
    -h|--help)
      helpme
      exit 0;;
    -l|--gitlab)
      host='gitlab.com'
      shift;;
    -t|--timeout)
      timeout="${2}"
      shift;shift;;
    -y|--noconfirm)
      noconfirm='true'
      shift;;
    -v|--verbose)
      verbosity='-x'
      shift;;
    -i|--install)
      if test "${2}" = "link"; then
        (set "${verbosity}"; eval "sudo cp --symbolic-link --verbose --update ${__file} /usr/local/bin/${__base}")
      elif test "${2}" = "hard"; then
        (set "${verbosity}"; eval "sudo cp --verbose --update ${__file} /usr/local/bin/${__base}")
      fi
      shift;shift;;
    -u|--uninstall)
      (set "${verbosity}"; set -u; eval "sudo rm -i /usr/local/bin/${__base}")
      shift;;
    -r|--revert)
      revoke
      shift;;
    *) # Unknown options, including username
      POSITIONAL+=("${1}") # Save it in an array for later
      shift;;
  esac
done

set -- "${POSITIONAL[@]}" # restore positional parameters

if test -n "${1}"; then
  if test "${noconfirm}" = "true"; then
    user="${1}"
    grant
  elif prompt "Would you like to give ${1} temporary ssh access to this computer?"; then
    user="${1}"
    grant
  else
    echo "Exiting..."
    exit 0
  fi
fi

exit 0
