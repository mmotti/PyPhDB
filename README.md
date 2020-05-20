# PyPhDB
This script has been created to interact with the Pi-hole database with the use of flat-files.

The view is that it will eventually export your adlists, whitelist, blacklist, whitelist regexps and blacklist regexps to plain text files for you to modify, and then re-import into the database.

### Current Functionality ###
Running this script will export the following files to **/etc/pihole/PyPhDB**:
* adlists.list
* whitelist.list
* blacklist.list
* whitelist_regex.list
* regex.list
* gravity.list

Import functionality is currently unavailable, but it may still serve useful in its current state for diagnostic purposes.

### Requirements ###
Python **3.6+** is required to run this script.

### Run the script ###
`curl -sSl https://raw.githubusercontent.com/mmotti/PyPhDB/master/PyPhDB.py | sudo python3`

### Manually remove output directory ###
`sudo rm -r /etc/pihole/PyPhDB`
