# **f**riendly **s**ecure **sh**ell
> Grant temporary SSH access to a trusted individual.

## Installation

```bash
git clone https://github.com/runarsf/fssh.git
cd fssh
./fssh.sh --install hard
```

## Usage

```bash
fssh --help
```

## How it works

FSSH grabs the public part of an SSH keypair from the public GitHub/GitLab API and adds it to `~/.ssh/authorized_keys`. When the script is terminated it restores the authorized_keys file without the changes made by the script. The backup file is stored at `~/.ssh/authorized_keys.bak`. Any changes made to the known_hosts file while the script is running will be discarded when the script is terminated.

> **fssh** © [runarsf](https://github.com/runarsf) · Author and maintainer.<br/>
> Released under the [GPLv3](https://opensource.org/licenses/GPL-3.0) [License](https://github.com/runarsf/fssh/blob/master/LICENSE).
