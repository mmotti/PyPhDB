# PyPhDB
This script has been created to give you the ability to quickly edit your **Adlists**, **Whitelist (Exact)**, **Whitelist (Regex)**, **Blacklist**, **Blacklist (Regex)** from flat-files (pre v5.0 behaviour).

### Requirements ###
* Python **3.6+** is required to run this script.
* Validators Python module (for adlist url validation)

#### Validators installation (required) ####
1. `sudo apt-get install python3-pip`
2. `sudo pip3 install validators`

### Docker ###
This script should work with Pi-hole being run within a docker container. In order to interact with your docker container, you must use the `--docker` switch **and** specify your Pi-hole directory volume using `--directory`

####Example:####

`curl -sSl https://raw.githubusercontent.com/mmotti/PyPhDB/master/PyPhDB.py | sudo python3 - --dump --docker --directory '/your/pihole/directory'`

### How to use ###

There are three main steps to this script:

#### dump ####
Dump the items from your Pi-hole DB to  **/etc/pihole/PyPhDB**

`curl -sSl https://raw.githubusercontent.com/mmotti/PyPhDB/master/PyPhDB.py | sudo python3 - --dump`

#### upload ####
Upload the changes to your Pi-hole DB

`curl -sSl https://raw.githubusercontent.com/mmotti/PyPhDB/master/PyPhDB.py | sudo python3 - --upload`

#### clean ####
Optional: Remove the **/etc/pihole/PyPhDB** directory.

`curl -sSl https://raw.githubusercontent.com/mmotti/PyPhDB/master/PyPhDB.py | sudo python3 - --clean`

### Further Information ###

This script will export the following files to **/etc/pihole/PyPhDB**: **adlists.list** (adlists), **whitelist.list** (exact whitelist), **blacklist.list** (exact blacklist), **whitelist_regex.list** (regex whitelist), **regex.list** (regex blacklist) and **gravity.list** (gravity domains)

Adlist urls, exact blacklist / whitelist domains and the regexps are validated before being allowed to enter the DB.

**gravity.list** is excluded from the upload process due to the way the entries are stored. This is dumped only for diagnostic purposes.

During the upload process, the script uses **INSERT OR IGNORE** to avoid issues caused by IDs changing etc. The script also determines entires that exist locally, but not in the database and will carefully remove them accordingly.
