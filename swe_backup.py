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


System Requirements:
    Stealthwatch Version: 7.0.0 or higher


Copyright (c) 2019, Cisco Systems, Inc. All rights reserved.
Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
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

# Object Prefix
OBJECT_PREFIX = ""

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

# If not hard coded, get the FMC IP, Username, and Password
if CONFIG_DATA['SMC_HOST'] == '':
    CONFIG_DATA['SMC_HOST'] = input("SMC IP Address: ")
if CONFIG_DATA['SMC_USER'] == '':
    CONFIG_DATA['SMC_USER'] = input("\nSMC Username: ")
if CONFIG_DATA['SMC_PASSWORD'] == '':
    CONFIG_DATA['SMC_PASSWORD'] = getpass.getpass("\nSMC Password: ")
if CONFIG_DATA['BACKUP_DIR'] == '':
    CONFIG_DATA['BACKUP_DIR'] = input("\nBACKUP Directory: ")

# Get the list of current backupped files
list_of_backups = os.listdir(CONFIG_DATA['BACKUP_DIR'])

# Set the URL for SMC login
url = "https://" + CONFIG_DATA['SMC_HOST'] +"/token/v2/authenticate"
print(url)

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

        for key in my_dict:
            my_list = ( list( my_dict.values() )[1] )

            list_filenames = []

            for filename in my_list:
                list_filenames.append(filename["fileName"])

            backup_list =[]

            # Check if file is already backuped and download if its not
            for file in list_filenames:
                if  not file in list_of_backups:
                    sys.stdout.write("From appliance " + id + " we are missing " + file + " downloading")
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
