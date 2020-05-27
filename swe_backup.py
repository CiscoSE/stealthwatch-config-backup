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
import json
import os
try:
    requests.packages.urllib3.disable_warnings()
except:
    pass

# Enter all authentication info
SMC_USER = ""
SMC_PASSWORD = ""
SMC_HOST = ""
BACKUP_DIR = ""

# Get the list of current backupped files
list_of_backups = os.listdir(BACKUP_DIR)

# Set the URL for SMC login
url = "https://" + SMC_HOST + "/token/v2/authenticate"

# Let's create the login request data
login_request_data = {
    "username": SMC_USER,
    "password": SMC_PASSWORD
}

# Initialize the Requests session
api_session = requests.Session()

# Perform the POST request to login
response = api_session.request("POST", url, verify=False, data=login_request_data)

# Continue if the login is successul
if(response.status_code == 200):

    # Set the url for getting the appliance list
    url = "https://" + SMC_HOST + "/cm/inventory/appliances/"

    # Perform the query to get the appliance list
    request_headers = {'Content-type': 'application/json', 'Accept': 'application/json'}
    response = api_session.request("GET", url, verify=False,)

    returned_data = json.loads(response.text)

    list_ids = []

    for SW_appliance in returned_data:
        list_ids.append(SW_appliance["id"])

    for id in list_ids:
        url = "https://" + SMC_HOST + "/cm/support/appliance/" + id + "/config-backup-file-list"
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
                    print("" + file + " has not been downloaded yet, downloading it now")
                    url = "https://" + SMC_HOST + "/cm/support/appliance/" + id + "/" + file + "/config-backup-file"
                    response = api_session.request("GET", url,  verify=False,)
                    myfilename = file
                    mydirname = BACKUP_DIR
                    myfullfilename = os.path.join(mydirname, myfilename)
                    zfile = open(myfullfilename, 'wb')
                    zfile.write(response.content)
                    zfile.close()
                else:
                    print("" + file + " has been downloaded already")
    url = 'https://' + SMC_HOST + '/token'
    response = api_session.delete(url, timeout=30, verify=False)


# If the login was unsuccessful
else:
        print("An error has ocurred, while logging in, with the following code {}".format(response.status_code))
