import requests
import json
from time import time
import csv
from datetime import datetime

# Globals
bearer = ""
inputFile = ""


"""
The config.json file looks like this:
{
  "bearerToken": "your bearer token here",
  "inputFile: "CSV path/filename with class info"
}
"""
# Read in the global variables from config.json
try:
    with open('./config.json', 'r') as reader:
        config = json.load(reader)
        bearer = config["bearerToken"]
        inputFile = config["inputFile"]
except:
    print("An exception occured reading in the config.json file.")


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
    headers = {'authorization': ('Bearer ' + (bearer)),
                   'content-type': 'application/json'}

    for eachMeeting in meetingsList:
        url = ("https://api.zoom.us/v2/meetings/" + eachMeeting["meeting"] + "?schedule_for_reminder=false&cancel_meeting_reminder=false")
        response = requests.request("DELETE", url, headers=headers, data=payload)
        print("Deleting :" + eachMeeting["meeting"] + " " +  str(response))



def main():

    # import meeting IDs from csv file into meetingsList array
    meetingsList = getCSV()
    meetingsReport = deleteMeetings(meetingsList)
   

if __name__ == "__main__":
    main()
