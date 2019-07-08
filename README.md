# fssh
> Grant temporary SSH access to a trusted individual.

## Prerequisites
* python3
* requirements.txt

## How it works
FSSH grabs the public part of an SSH keypair from the public GitHub API and adds it to `~/.ssh/known_hosts`. When the script is terminated it restores the known_hosts file without the changes made by the script. The backup file is stored at `~/.ssh/known_hosts_fssh`. Any changes made to the known_hosts file while the script is running will be discarded when the script is terminated.

## Author

**fssh** © [runarsf](https://github.com/runarsf), Released under the [GPLv3](https://github.com/runarsf/fssh/blob/master/LICENSE) License.<br>
Authored and maintained by runarsf.
