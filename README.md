
# Bitlocker OSX Unlocker


## Description

This python program takes a Bitlocker-encrypted drive that is encypted with a password and uses Dislocker to mount the drive and allow its contents to be viewed. It basically just makes Disklocker that much easier to use for OSX users.

## Note

This program only supports Bitlocker drives that are only encrypted with a password but NOT a key.
Also, you must be root to run this.

## Prerequisites

1. Python 2.7
2. Dislocker (https://github.com/Aorimn/dislocker)
3. NTFS-3G (https://sourceforge.net/projects/ntfs-3g/) - this is if you want to read AND write files on the drive instead of just reading them.

## Usage
```bash
$ python bitlocker_unlocker_osx.py
```
