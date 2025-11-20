# Packages

Repository for all the packages sent over TCP socket.
You can include the packages into a repository with:
```bash
git submodule add https://github.com/affix-3d-robot-control/packages.git ./packages
```

To download the packages in a repository where it is already added, run:
```bash
git submodule update --recursive --init
```

To update the downloaded package repository to the latest commit, run:
```bash
git submodule update --recursive --remote
```
