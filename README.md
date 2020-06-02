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
2. Download the files cognitive-intelligence-syslog-exporter.py and requirements.txt
3. Install the necessary python modules with the command: pip install -r requirements.txt
- ensure you use the correct pip executable for your instance of Python 3

Alternatively, advanced users can also use git to checkout / clone this project.

## Configuration

Open the desired .py file that you intend to run and enter the following values where specified:
   ```
   SMC_USER = ""
   SMC_PASSWORD = ""
   SMC_HOST = ""
   BACKUP_DIR = "" (Please use full path)
   ```
## Usage

1. Identify the path to your Python 3 executible.
Depending how Python 3 was installed, this might be as simple as just calling the command python or python3.
2. Run the Python script with the following command:
  $ <PYTHON-PATH> <PYTHON-SCRIPT-PATH>
  Example: $ /usr/bin/python ./swe_backup.py


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
