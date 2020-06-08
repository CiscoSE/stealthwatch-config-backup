#!/usr/bin/env python

"""
This script will download all the config backups from the SMC off all applinaces
It will check if the backup has already been downloaded, if so it will skip it
Next version will also have a rotate option build in

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

import requests
import getpass
import json
import sys
import os
try:
    requests.packages.urllib3.disable_warnings()
except:
    pass

# Config Paramters
CONFIG_FILE     = "config.json"
CONFIG_DATA     = None

# A function to load CONFIG_DATA from file
def loadConfig():

    global CONFIG_DATA

    sys.stdout.write("\n")
    sys.stdout.write("Loading config data...")
    sys.stdout.write("\n")

    # If we have a stored config file, then use it, otherwise create an empty one
    if os.path.isfile(CONFIG_FILE):

        # Open the CONFIG_FILE and load it
        with open(CONFIG_FILE, 'r') as config_file:
            CONFIG_DATA = json.loads(config_file.read())

        sys.stdout.write("Config loading complete.")
        sys.stdout.write("\n")
        sys.stdout.write("\n")

    else:

        sys.stdout.write("Config file not found, loading empty defaults...")
        sys.stdout.write("\n")
        sys.stdout.write("\n")

        # Set the CONFIG_DATA defaults
        CONFIG_DATA = {
            "SMC_HOST": "",
            "SMC_USER": "",
            "SMC_PASSWORD": "",
            "BACKUP_DIR": "",
        }

# A function to store CONFIG_DATA to file
def saveConfig():

    sys.stdout.write("Saving config data...")
    sys.stdout.write("\n")

    with open(CONFIG_FILE, 'w') as output_file:
        json.dump(CONFIG_DATA, output_file, indent=4)

# Load config data from file
loadConfig()

# If not hard coded, get the SMC IP, Username, Password and Backup Directory
if CONFIG_DATA['SMC_HOST'] == '':
    CONFIG_DATA['SMC_HOST'] = input("SMC IP Address: ")
if CONFIG_DATA['SMC_USER'] == '':
    CONFIG_DATA['SMC_USER'] = input("\nSMC Username: ")
if CONFIG_DATA['SMC_PASSWORD'] == '':
    CONFIG_DATA['SMC_PASSWORD'] = getpass.getpass("\nSMC Password: ")
if CONFIG_DATA['BACKUP_DIR'] == '':
    CONFIG_DATA['BACKUP_DIR'] = input("\nBACKUP Directory: ")

## Save the Config
saveConfig()

# Get the list of current backupped files
sys.stdout.write("\n")
sys.stdout.write("Get the list all already backupped files")
sys.stdout.write("\n")

list_of_backups = os.listdir(CONFIG_DATA['BACKUP_DIR'])

# Set the URL for SMC login
url = "https://" + CONFIG_DATA['SMC_HOST'] +"/token/v2/authenticate"

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
    print("Getting the appliance list")
    url = "https://" + CONFIG_DATA['SMC_HOST'] +"/cm/inventory/appliances/"

    # Perform the query to get the appliance list

    sys.stdout.write("\n")
    sys.stdout.write("Getting the appliance list")
    sys.stdout.write("\n")

    request_headers = {'Content-type': 'application/json', 'Accept': 'application/json'}
    response = api_session.request("GET", url, verify=False,)

    returned_data = json.loads(response.text)

    list_ids = []

    for SW_appliance in returned_data:
        list_ids.append(SW_appliance["id"])

    for id in list_ids:
        url = "https://" + CONFIG_DATA['SMC_HOST'] +"/cm/support/appliance/" + id + "/config-backup-file-list"
        response = api_session.request("GET", url,  verify=False,)

        returned_data = json.loads(response.text)
        my_dict = returned_data

        sys.stdout.write("\n")
        sys.stdout.write("Downloading backups for appliance with ID: ")
        sys.stdout.write(id)
        sys.stdout.write("\n")

        for key in my_dict["configBackups"]:
            list_filenames = []

            list_filenames.append(key["fileName"])

            for file in list_filenames:
                if  not file in list_of_backups:
                    sys.stdout.write("\n")
                    sys.stdout.write("" + file + " has not been downloaded yet, downloading it now")
                    sys.stdout.write("\n")

                    url = "https://" + CONFIG_DATA['SMC_HOST'] +"/cm/support/appliance/" + id + "/" + file + "/config-backup-file"
                    response = api_session.request("GET", url,  verify=False,)
                    myfilename = file
                    mydirname = CONFIG_DATA['BACKUP_DIR']
                    myfullfilename = os.path.join(mydirname, myfilename)
                    zfile = open(myfullfilename, 'wb')
                    zfile.write(response.content)
                    zfile.close()
                else:
                    sys.stdout.write("" + file + " has been downloaded already")
                    sys.stdout.write("\n")
    url = "https://" + CONFIG_DATA['SMC_HOST'] +"/token"
    response = api_session.delete(url, timeout=30, verify=False)


# If the login was unsuccessful
else:
        print("An error has ocurred, while logging in, with the following code {}".format(response.status_code))
