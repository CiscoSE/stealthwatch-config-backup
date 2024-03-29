# Stealthwatch Enterprise Config Backup

[![published](https://static.production.devnetcloud.com/codeexchange/assets/images/devnet-published.svg)](https://developer.cisco.com/codeexchange/github/repo/CiscoSE/stealthwatch-config-backup)

This script will downloaded all config backups from the Stealthwatch Enterprise Central Manager,
for all the appliances managed by Stealthwatch Enterprise Central Manager.

All appliances need to be reachable with ICMP from the server where this script is installed for the script to work properly.

It will not create a backup of the flow data on every Flow Collector.
The script will only download the config backups. The script does not remove any backups from the path where the backups are downloaded to.

This script is available for use by the Cisco DevNet community through Code Exchange. For more information on the Stealthwatch Enterprise REST API, please see the following link: https://developer.cisco.com/docs/stealthwatch/enterprise/

## Release notes

Version 1.0.0  
- Initial release

Version 1.1.2  
- Start using a logfile  
- WebEx Teams support  
- Email of logfile  

Version 1.1.3
- Added check to see if all appliances are up and reachable.

## Use Case Description

This script uses the Stealthwatch Enterprise API's to download all backups files present in Central Management.  
By using this script the backups files can be stored outside the Stealthwatch environment for save keeping.


## Installation

1. Ensure Python 3 is installed
   - To download and install Python 3, please visit https://www.python.org
2. Download the files [swe_backup.py](https://github.com/CiscoSE/stealthwatch-config-backup/blob/master/swe_backup.py), [requirements.txt](https://github.com/CiscoSE/stealthwatch-config-backup/blob/master/requirements.txt) and [config.json](https://github.com/CiscoSE/stealthwatch-config-backup/blob/master/config.json)
3. Install the necessary python modules with the command: ``` pip install -r requirements.txt ```
   - ensure you use the correct pip executable for your instance of Python 3
4. Stealthwatch user credentials with the "Master Admin" role assigned.
   - User roles are configured in the Stealthwatch web interface. Simply navigate to _Global Settings -> User Management_.
5. It is possible to integrate the script with Webex Teams. In order to do that, an API Access Token (WEBEX_ACCESS_TOKEN) and a Room ID (WEBEX_ROOM_ID need to be entered in the config.json file. Please retrieve your key from: https://developer.webex.com/docs/api/getting-started. Then create a dedicated Webex Teams space for these notifications and retrieve the Room ID from: https://developer.webex.com/docs/api/v1/rooms/list-rooms. Please be aware that the personal token from the getting started page only works for 12 hours. To be able to have a key that works longer then 12 hours its recommended to leverage a [Webex Teams bot](https://developer.webex.com/my-apps/new/bot) and invite that bot to a  room for the notifications.
6. It is also possible to have the script send it log file (swe_backup.log) using email. For this you need to configure the options Email subject (MAIL_SUBJECT), adress to send email to (TO_EMAIL), from email address (FROM_EMAIL), and SMPT Server to us (SMTP_SERVER) in config.json.


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
It is recommended to create a separate SMC login account for API usage, otherwise the admin will be logged out during every API call. Add the IP of the SMC (SMC_IP), the username (SMC_USER), password (SMC_PASSWORD) and the path where the backups needs to be stored (BACKUP_DIR) to the config.json file. If you do not add anything, you will be prompted to fill this in when executing the script.  
_Its recommended to create unique credentials for scripting/API purposes._

## Testing

If you want to test this script before using it in a production environment you can leverage the [DevNet Stealthwatch Sandbox Environment](https://devnetsandbox.cisco.com/RM/Diagram/Index/3c832112-cf88-4e74-a439-6fdb47a5882e?diagramType=Topology)

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
     - Example crontab entry to run the script everyday at 0:25
       - ``` 25 0 * * * /usr/bin/env bash -c 'cd <path to stealthwatch-config-backup> && source <path to stealthwatch-config-backup>/venv/bin/activate && <path to stealthwatch-config-backup>/venv/bin/python swe_backup.py' > /dev/null 2>&1 ```

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
  - For worldwide support numbers: [www.cisco.com/en/US/partner/support/tsd_cisco_worldwide_contacts.html](https://www.cisco.com/c/en/us/support/web/tsd-cisco-worldwide-contacts.html)
  - If you don't have a Cisco service contract, send an email to swatchc-support@cisco.com describing your problem.

## Docker Container

This script is Docker friendly, and can be run as a container.  
When running it from a container it its best to store the backups and the logs file outside the container for easy access.

To build the container, run the script once to populate the config.json file, or manually populate the configuration variables.  
To make sure the below ```docker run``` command work please set the ```BACKUP_DIR``` to ```/backups```

Once the config.json file is populated, run the following command to build the container:

``` docker build -t swe_backup_config . ```

You can then run the container as a daemon with the following command, for storage of the backups and logs files outside of the container.  
You can add -rm to the command to automatically have the container removed after run:

``` docker run -d  -it --name swe_backup_config --mount type=bind,source="<path to where to store backups>",target="/backups" --mount type=bind,source="<path to where to store logs>",target="/logs" ```


## Getting involved

Contributions to this code are welcome and appreciated. See [CONTRIBUTING](https://github.com/CiscoDevNet/cognitive-intelligence-syslog-exporter/blob/master/CONTRIBUTING.md) for details. Please adhere to our [Code of Conduct](https://github.com/CiscoDevNet/cognitive-intelligence-syslog-exporter/blob/master/CODE_OF_CONDUCT.md) at all times.

## License info

This code is licensed under the BSD 3-Clause License... see [LICENSE](https://github.com/CiscoDevNet/cognitive-intelligence-syslog-exporter/blob/master/LICENSE) for details

## Author(s)

This project was written and is maintained by the following individuals:

* Ramon Weeling <rweeling@cisco.com>
* Christopher van der Made <chrivand@cisco.com>
* Kyle Winters <kywinters@cisco.com>
