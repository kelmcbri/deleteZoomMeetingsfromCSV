import jwt
from jwt import encode
import requests
import json
from time import time
import csv
from datetime import datetime

# Globals
bearer = ""
API_KEY = ""
API_SEC = ""
inputFile = ""
outputFileJSON = ""
outputFileCSV = ""


"""
Load the keys from config.json file
The config.json file looks like this:
{
  "bearerToken": "your bearer token here",
  "API_KEY": "",
  "API_SEC": "",
  "inputFile: "CSV path/filename with class info",
  "outputFileJSON": "JSON path/filename with combined saba zoom info",
  "outputFileCSV": "CSV path/filename with combined saba zoom info"
}

NOTE - if you are using your JWT bearer Token, you should leave
        API_KEY and API_SEC as ''
"""
# Read in the global variables from config.json
try:
    with open('./config.json', 'r') as reader:
        config = json.load(reader)
        bearer = config["bearerToken"]
        API_KEY = config["API_KEY"]
        API_SEC = config["API_SEC"]
        inputFile = config["inputFile"]
        outputFileJSON = config["outputFileJSON"]
        outputFileCSV = config["outputFileCSV"]
except:
    print("An exception occured reading in the config.json file.")

# Generate a token using the pyjwt library

def generateToken():
    token = jwt.encode(
        # Create a payload of the token containing API Key & expiration time
        {'iss': API_KEY, 'exp': time() + 5000},
        # Secret used to generate token signature
        API_SEC,
        # Specify the hashing alg
        algorithm='HS256'
        # Convert token to utf-8
    )
    return token
    # send a request with headers including a token


""" Read in list of meetings from saba file
    Create Array of meetings to be created on zoom

Input file is determined by "inputFile" field in ./config.json file.
The input file must be in CSV format.

"""


def getCSV():
    print("\nReading CSV data from file " + (inputFile))
    meetingDetails = []

    with open(inputFile) as csvfile:
        csvReader = csv.DictReader(csvfile)
        for rows in csvReader:
            meetingDetails.append(
                {"meeting": rows["meeting"]}
                )

        # print(meetingDetails)
        return(meetingDetails)

def deleteMeetings(meetingsList):
    print("\nDeleting Zoom Meetings")
    payload = {}
    if bearer != "":
        headers = {'authorization': ('Bearer ' + (bearer)),
                   'content-type': 'application/json'}
    else:
        headers = {'authorization': 'Bearer %s' % generateToken(),
                   'content-type': 'application/json'}

    for eachMeeting in meetingsList:
        url = ("https://api.zoom.us/v2/meetings/" + eachMeeting["meeting"] + "?schedule_for_reminder=false&cancel_meeting_reminder=false")
        response = requests.request("DELETE", url, headers=headers, data=payload)



def main():

    # import meeting info from csv file into meetingsList array
    meetingsList = getCSV()
    meetingsReport = deleteMeetings(meetingsList)

if __name__ == "__main__":
    main()
