#!/usr/bin/env bash
set -o errexit
set -o pipefail
set -o noclobber
finish() {

}
trap finish INT

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
	Usage: deploy [options] [commands]
 
	Options:
	  -d, --dotfiles <directory>  Dotfiles directory.
	  -p, --packages <file>       Package candidate file.
	  -n, --no-backup             Disable backup.
 
 Commands:
	  full                        Install packages and deploy configs.
	  packages                    Install packages.
	  configs                     Deploy configs.
 
	Examples:
	  deploy -p ../deploy.json packages
	  deploy -d ../ configs
	  deploy --dotfiles ../ --packages ../deploy.json full
	EOMAN
}
 
test "${#}" -lt "1" && "${0}" --help
POSITIONAL=()
while [[ $# -gt 0 ]]; do
  case "${1}" in
    -h|--help)
      helpme
      shift;;
    *) # Unknown options
      POSITIONAL+=("${1}") # Save it in an array for later
      shift;;
  esac
done
 
set -- "${POSITIONAL[@]}" # restore positional parameters
 
if test -n "${1}"; then
    prompt "Would you like to give ${1} temporary ssh access to this computer?"
fi