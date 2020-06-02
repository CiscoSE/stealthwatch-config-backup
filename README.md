# Stealthwatch Config Backup

This script will downloaded all config backups from the Stealthwatch Enterprise Central Manager,
for all the appliances managed by Stealthwatch Enterprise Central Manager.

It will not create a backup of the flow data on every Flow Collector.

## Use Case Description

This script uses the Stealthwatch Enterprise API's to download all backups files present on Central Management.
By doing this the backups files can be stored outside the Stealthwatch environment for save keeping.

## Installation

1. Ensure Python 3 is installed
   - To download and install Python 3, please visit https://www.python.org
2. Download the files swe_backup.py and requirements.txt
3. Install the necessary python modules with the command: ``` pip install -r requirements.txt ```
   - ensure you use the correct pip executable for your instance of Python 3

Alternatively, advanced users can also use git to checkout / clone this project.

## Configuration

The file env.conf will be generated upon your first run of the script, and will contain the following fields:

```
[STEALTHWATCH]
SMC = (The IP address of the SMC)
USER = (The username on the SMC to use, with 'Master Admin' role)
PASSWORD = (Encrypted password string [encryption handled on initial config])
BACKUP_DIR = (Location where the backup files will be downloaded to)
```

## Usage

1. Identify the path to your Python 3 executible
   - Depending how Python 3 was installed, this might be as simple as just calling the command python or python3
2. Run the Python script with the following command:
   - $ <PYTHON-PATH> swe_backup.py
   - Example: $ /usr/bin/python ./swe_backup.py
3. If running for the first time, enter the request configuration items when prompted
4. This script is designed to be run as a cronjob after the initial run... it caches the previous run's timestamp and only pulls events that are new or have been updated since the last run
   - To schedule a cronjob, run the command crontab -e and add a new line containing: 0 0/10 * * * <path-to-python-script>
     - [More info on how to use crontab](https://opensource.com/article/17/11/how-use-cron-linux)

## Known issues

No known issues.

## Getting help

Use this project at your own risk (support not provided)... If you need technical support with Cisco Stealthwatch APIs, do one of the following:

Browse the Forum
Check out our forum to pose a question or to see if any questions have already been answered by our community... we monitor these forums on a best effort basis and will periodically post answers

Open A Case
To open a case by web: http://www.cisco.com/c/en/us/support/index.html
To open a case by email: tac@cisco.com
For phone support: 1-800-553-2447 (U.S.)
For worldwide support numbers: www.cisco.com/en/US/partner/support/tsd_cisco_worldwide_contacts.html
If you don't have a Cisco service contract, send an email to swatchc-support@cisco.com describing your problem.

## Getting involved

Contributions to this code are welcome and appreciated. See CONTRIBUTING for details. Please adhere to our Code of Conduct at all times.

## Author(s)

This project was written and is maintained by the following individuals:

* Ramon Weeling <rweeling@cisco.com>
* Christopher van der Made <chrivand@cisco.com>
* Kyle Winters <kywinters@cisco.com>
