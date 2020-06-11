# Stealthwatch Enterprise Config Backup

[![published](https://static.production.devnetcloud.com/codeexchange/assets/images/devnet-published.svg)](https://developer.cisco.com/codeexchange/github/repo/CiscoSE/stealthwatch-config-backup)

This script will downloaded all config backups from the Stealthwatch Enterprise Central Manager,
for all the appliances managed by Stealthwatch Enterprise Central Manager.

It will not create a backup of the flow data on every Flow Collector.
The script will only download the config backups. And the script does not remove any backups from the path where the backups are downloaded to.


## Use Case Description

This script uses the Stealthwatch Enterprise API's to download all backups files present on Central Management.  
By using this script the backups files can be stored outside the Stealthwatch environment for save keeping.

## Installation

1. Ensure Python 3 is installed
   - To download and install Python 3, please visit https://www.python.org
2. Download the files [swe_backup.py](https://github.com/CiscoSE/stealthwatch-config-backup/blob/master/swe_backup.py), [requirements.txt](https://github.com/CiscoSE/stealthwatch-config-backup/blob/master/requirements.txt) and [config.json](https://github.com/CiscoSE/stealthwatch-config-backup/blob/master/config.json)
3. Install the necessary python modules with the command: ``` pip install -r requirements.txt ```
   - ensure you use the correct pip executable for your instance of Python 3
4. Stealthwatch user credentials with the "Master Admin" role assigned.
   - User roles are configured in the Stealthwatch web interface. Simply navigate to _Global Settings -> User Management_.


_Alternatively, advanced users can also use git to checkout / clone this project._


1. Clone the repo
   - ``` git clone https://github.com/CiscoSE/stealthwatch-config-backup ```

2. cd into directory
   - ``` cd stealthwatch-config-backup ```

3. Create the virtual environment in a sub dir in the same directory
   - ``` python3 -m venv venv ```

4. Start the virtual environment and install requirements.txt
   - ``` source venv/bin/activate ```
   - ``` pip install -r requirements.txt ```

5. Execute the script as any other Python script form console. Check the reachability to SMC before executing this script. Script is tested on SMC 7.0 and higher.
   - ``` python swe_backup.py ```

## Configuration

You need the IP address of the SMC, the username, password and the full path of where the script will download all the backup files.
It is recommended to create a separate SMC login account for API usage, otherwise the admin will be logged out during every API call. Add the IP of the SMC, the username, password and the path to the config.json file. If you do not add anything, you will be prompted to fill this in when executing the script.  
_Its recommended to create unique credentials for scripting/API purposes._

## Testing

If you want to test this script before using it in a production enviroment you can leverage the [DevNet Stealthwatch Sandbox Enviroment](https://devnetsandbox.cisco.com/RM/Diagram/Index/3c832112-cf88-4e74-a439-6fdb47a5882e?diagramType=Topology)

## Usage

1. Identify the path to your Python 3 executable
   - Depending how Python 3 was installed, this might be as simple as just calling the command ``` python ``` or ``` python3 ```
2. Run the Python script with the following command:
   - ``` $ <PYTHON-PATH> swe_backup.py ```
   - Example: ``` $ /usr/bin/python ./swe_backup.py ```
3. If running for the first time, enter the request configuration items when prompted
4. This script is designed to be run as a cronjob after the initial run... it caches the previous run's timestamp and only pulls events that are new or have been updated since the last run
   - To schedule a cronjob, run the command crontab -e and add a new line containing: ``` 0 0/10 * * * <path-to-python-script> ```
     - [More info on how to use crontab](https://opensource.com/article/17/11/how-use-cron-linux)

## Known issues

No known issues

## Getting help

Use this project at your own risk (support not provided)... _If you need technical support with Cisco Stealthwatch APIs, do one of the following:_

__Browse the Forum__

Check out our [forum](https://community.cisco.com/t5/custom/page/page-id/customFilteredByMultiLabel?board=j-disc-dev-security&labels=stealthwatch) to pose a question or to see if any questions have already been answered by our community... we monitor these forums on a best effort basis and will periodically post answers

__Open A Case__
  - To open a case by web: [http://www.cisco.com/c/en/us/support/index.html](http://www.cisco.com/c/en/us/support/index.html)
  - To open a case by email: tac@cisco.com
  - For phone support: 1-800-553-2447 (U.S.)
  - For worldwide support numbers: [www.cisco.com/en/US/partner/support/tsd_cisco_worldwide_contacts.html](www.cisco.com/en/US/partner/support/tsd_cisco_worldwide_contacts.html)
  - If you don't have a Cisco service contract, send an email to swatchc-support@cisco.com describing your problem.

## Getting involved

Contributions to this code are welcome and appreciated. See [CONTRIBUTING](https://github.com/CiscoDevNet/cognitive-intelligence-syslog-exporter/blob/master/CONTRIBUTING.md) for details. Please adhere to our [Code of Conduct](https://github.com/CiscoDevNet/cognitive-intelligence-syslog-exporter/blob/master/CODE_OF_CONDUCT.md) at all times.

## License info

This code is licensed under the BSD 3-Clause License... see [LICENSE](https://github.com/CiscoDevNet/cognitive-intelligence-syslog-exporter/blob/master/LICENSE) for details


## Author(s)

This project was written and is maintained by the following individuals:

* Ramon Weeling <rweeling@cisco.com>
* Christopher van der Made <chrivand@cisco.com>
* Kyle Winters <kywinters@cisco.com>
