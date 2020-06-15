#!/usr/bin/env python

"""
This script will download all the config backups from the SMC off all applinaces
It will check if the backup has already been downloaded, if so it will skip it
Next version will also have a rotate option build in

Version 1.0.0
    - Inital release

Version 1.1.2
    - Start using a logfile
        The script will create a new logfile for each day and keep 7  days of logs
    - WebEx Teams support
    - Email of logfile

For more information on this API, please visit:
https://developer.cisco.com/docs/stealthwatch/

Script Dependencies:
    requests, json, os
Depencency Installation:
    $ pip install requests
    $ pip install json
    $ pip install os
    $ pip install sys
    $ pip install getpass
    $ pip install datetime
    $ pip install webexteamssdk
    $ pip install smtplib
    $ pip install logging

System Requirements:
    Stealthwatch Version: 7.0.0 or higher

Copyright (c) 2020 Cisco and/or its affiliates.

This software is licensed to you under the terms of the Cisco Sample
Code License, Version 1.0 (the "License"). You may obtain a copy of the
License at

               https://developer.cisco.com/docs/licenses

All use of the material herein must be in accordance with the terms of
the License. All rights not expressly granted by the License are
reserved. Unless required by applicable law or agreed to separately in
writing, software distributed under the License is distributed on an "AS
IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
or implied.
"""

__author__ = "Ramon Weeling"
__email__ = "rweeling@cisco.com"
__version__ = "1.1.2"
__copyright__ = "Copyright (c) 2020 Cisco and/or its affiliates."
__license__ = "Cisco Sample Code License, Version 1.1"

import requests
import getpass
import json
import sys
import os
import datetime
import webexteamssdk
import logging
import logging.handlers
import smtplib
try:
    requests.packages.urllib3.disable_warnings()
except:
    pass

# gets log path (and creates log directory if it doesn't already exist)
log_directory = "{}/logs".format(os.path.dirname(os.path.abspath(__file__)))
if not os.path.isdir(log_directory):
    os.mkdir(log_directory)
log_file = 'swe_backup.log'
log_path = os.path.join(log_directory, log_file)
# creates the log handler in case the default move does not work
handler = logging.handlers.TimedRotatingFileHandler(log_path,'midnight',7)
handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)-s -- %(module)s:%(lineno)d - %(message)s'))
# creates the logger
logger = logging.getLogger(log_file[-4])
logger.setLevel('INFO')
logger.addHandler(handler)

log_file_email = log_path

# Put begin date and time in logfile
start_timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

logger.info("---------------------------------------------------------------------")
logger.info("Script started at " + start_timestamp + "")

# Config Paramters
CONFIG_FILE     = "config.json"
CONFIG_DATA     = None

# A function to load CONFIG_DATA from file
def loadConfig():

    global CONFIG_DATA
    logger.info("Loading config data...")

    # If we have a stored config file, then use it, otherwise create an empty one
    if os.path.isfile(CONFIG_FILE):

        # Open the CONFIG_FILE and load it
        with open(CONFIG_FILE, 'r') as config_file:
            CONFIG_DATA = json.loads(config_file.read())
        logger.info("Config loading complete.")

    else:
        logger.info("Config file not found, loading empty defaults...")

        # Set the CONFIG_DATA defaults
        CONFIG_DATA = {
            "SMC_IP": "",
            "SMC_USER": "",
            "SMC_PASSWORD": "",
            "BACKUP_DIR": "",
            "FROM_EMAIL": "",
            "TO_EMAIL": "",
            "EMAIL_SUBJECT": "",
        }

# A function to store CONFIG_DATA to file
def saveConfig():

    logger.info("Saving config data...")

    with open(CONFIG_FILE, 'w') as output_file:
        json.dump(CONFIG_DATA, output_file, indent=4)

# Load config data from file
loadConfig()

# If not hard coded, get the SMC IP, Username, Password and Backup Directory
if CONFIG_DATA['SMC_IP'] == '':
    CONFIG_DATA['SMC_IP'] = input("SMC IP Address: ")
if CONFIG_DATA['SMC_USER'] == '':
    CONFIG_DATA['SMC_USER'] = input("\nSMC Username: ")
if CONFIG_DATA['SMC_PASSWORD'] == '':
    CONFIG_DATA['SMC_PASSWORD'] = getpass.getpass("\nSMC Password: ")
if CONFIG_DATA['BACKUP_DIR'] == '':
    CONFIG_DATA['BACKUP_DIR'] = input("\nBACKUP Directory: ")

## Save the Config
saveConfig()

# Get the list of current backupped files that are already downloaded
logger.info("Getting the list off all already downloaded backup files")

list_of_backups = os.listdir(CONFIG_DATA['BACKUP_DIR'])

# Set the URL for SMC login
url = "https://" + CONFIG_DATA['SMC_IP'] +"/token/v2/authenticate"

logger.info("Stealthwatch Authentication URL: {}".format(url))

# Let's create the login request data
login_request_data = {
    "username": CONFIG_DATA['SMC_USER'],
    "password": CONFIG_DATA['SMC_PASSWORD']
}

# Initialize the Requests session
api_session = requests.Session()

# Perform the POST request to login
response = api_session.request("POST", url, verify=False, data=login_request_data)

# Continue if the login is successul
if(response.status_code == 200):

    # Set the url for getting the appliance list
    url = "https://" + CONFIG_DATA['SMC_IP'] +"/cm/inventory/appliances/"

    # Perform the query to get the appliance list

    logger.info("Getting the appliance list")

    request_headers = {'Content-type': 'application/json', 'Accept': 'application/json'}
    response = api_session.request("GET", url, verify=False,)

    returned_data = json.loads(response.text)

    list_ids = []

    for SW_appliance in returned_data:
        list_ids.append(SW_appliance["id"])

    for id in list_ids:
        url = "https://" + CONFIG_DATA['SMC_IP'] +"/cm/support/appliance/" + id + "/config-backup-file-list"
        response = api_session.request("GET", url,  verify=False,)

        returned_data = json.loads(response.text)
        config_backup_file_list = returned_data

        logger.info("Downloading backups for appliance with ID:")

        for key in config_backup_file_list["configBackups"]:
            list_filenames = []

            list_filenames.append(key["fileName"])

            for file in list_filenames:
                if  not file in list_of_backups:

                    logger.info("" + file + " has not been downloaded yet, downloading it now")

                    # if Webex Teams tokens set, then send message to Webex room
                    if CONFIG_DATA['WEBEX_ACCESS_TOKEN'] == '' or CONFIG_DATA['WEBEX_ROOM_ID'] == '':

                        # user feed back
                        logger.info("Webex Teams not set, not sending updates about new download to Webex Teams")
                    else:
                            message_text = f"" + file + " has not been downloaded yet, downloading it now"

                            # instantiate the Webex handler with the access token
                            teams = webexteamssdk.WebexTeamsAPI(CONFIG_DATA['WEBEX_ACCESS_TOKEN'])

                            # post a message to the specified Webex room
                            message = teams.messages.create(CONFIG_DATA['WEBEX_ROOM_ID'], text=message_text)

                    url = "https://" + CONFIG_DATA['SMC_IP'] +"/cm/support/appliance/" + id + "/" + file + "/config-backup-file"


                    response = api_session.request("GET", url,  verify=False,)
                    myfilename = file
                    mydirname = CONFIG_DATA['BACKUP_DIR']
                    myfullfilename = os.path.join(mydirname, myfilename)
                    zfile = open(myfullfilename, 'wb')
                    zfile.write(response.content)
                    zfile.close()
                else:
                    logger.info("" + file + " has been downloaded already")

    url = "https://" + CONFIG_DATA['SMC_IP'] +"/token"
    response = api_session.delete(url, timeout=30, verify=False)

# If the login was unsuccessful
else:
        logger.info("An error has ocurred, while logging in, with the following code {}".format(response.status_code))

        # if Webex Teams tokens set, then send error message to Webex room
        if CONFIG_DATA['WEBEX_ACCESS_TOKEN'] == '' or CONFIG_DATA['WEBEX_ROOM_ID'] == '':
            # user feed back
            logger.info("Webex Teams not set, not sending updates to Webex Teams")
        else:
            message_text = f"Error occurred with the following status code: {response.status_code}"

            # instantiate the Webex handler with the access token
            teams = webexteamssdk.WebexTeamsAPI(CONFIG_DATA['WEBEX_ACCESS_TOKEN'])

            # post a message to the specified Webex room
            message = teams.messages.create(CONFIG_DATA['WEBEX_ROOM_ID'], text=message_text)
            quit()

# End with and date and time in log file
end_timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
logger.info("Script ended at " + end_timestamp + "")

# if Webex Teams tokens set, then send message to Webex room that the script has finnished
if CONFIG_DATA['WEBEX_ACCESS_TOKEN'] == '' or CONFIG_DATA['WEBEX_ROOM_ID'] == '':
    # user feed back
    logger.info("Webex Teams not set, not sending updates to Webex Teams")
else:
    message_text = f"Script finnished, please see the logging in swe_backup.log"

    # instantiate the Webex handler with the access token
    teams = webexteamssdk.WebexTeamsAPI(CONFIG_DATA['WEBEX_ACCESS_TOKEN'])

    # post a message to the specified Webex room
    message = teams.messages.create(CONFIG_DATA['WEBEX_ROOM_ID'], text=message_text)


# Send the log file using Email if configured

if CONFIG_DATA['EMAIL_SUBJECT'] == '' or CONFIG_DATA['FROM_EMAIL'] == '' or CONFIG_DATA['FROM_EMAIL'] == '' or CONFIG_DATA['TO_EMAIL'] == '' or CONFIG_DATA['SMTP_SERVER'] == '':
    # user feed back
    logger.info("Email not configered not sending the log file in email.")
    # if Webex Teams tokens set, then send message to Webex room that the script has finnished
    if CONFIG_DATA['WEBEX_ACCESS_TOKEN'] == '' or CONFIG_DATA['WEBEX_ROOM_ID'] == '':
        # user feed back
        logger.info("Webex Teams not set, not sending updates to Webex Teams")
    else:
        message_text = f"Email not configered not sending the log file in email."

        # instantiate the Webex handler with the access token
        teams = webexteamssdk.WebexTeamsAPI(CONFIG_DATA['WEBEX_ACCESS_TOKEN'])

        # post a message to the specified Webex room
        message = teams.messages.create(CONFIG_DATA['WEBEX_ROOM_ID'], text=message_text)

else:
    # user feed back
    logger.info("Email configered sending log file using email.")

    # if Webex Teams tokens set, then send message to Webex room that the script has finnished
    if CONFIG_DATA['WEBEX_ACCESS_TOKEN'] == '' or CONFIG_DATA['WEBEX_ROOM_ID'] == '':
        # user feed back
        logger.info("Webex Teams not set, not sending updates to Webex Teams")
    else:
        message_text = f"Email is configured so I'm sending log file using email."

        # instantiate the Webex handler with the access token
        teams = webexteamssdk.WebexTeamsAPI(CONFIG_DATA['WEBEX_ACCESS_TOKEN'])

        # post a message to the specified Webex room
        message = teams.messages.create(CONFIG_DATA['WEBEX_ROOM_ID'], text=message_text)

    from email.message import EmailMessage
    msg_body = "Please find the log file attached \n your local config backup script \n \n \n"

    msg = EmailMessage()

    msg['Subject'] = (CONFIG_DATA['EMAIL_SUBJECT'])
    msg['From'] = (CONFIG_DATA['FROM_EMAIL'])
    msg['To'] = (CONFIG_DATA['TO_EMAIL'])

    msg.set_content(msg_body)

    if os.path.isfile(log_file_email):
        msg.add_attachment(open(log_file_email, "r").read(), filename=os.path.basename(log_file_email))


        # Send the message via our own SMTP server.
        s = smtplib.SMTP(CONFIG_DATA['SMTP_SERVER'])
        s.send_message(msg)
        s.quit()
