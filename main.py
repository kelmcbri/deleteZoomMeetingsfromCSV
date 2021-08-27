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
                {
                    "host": rows["host"],
                    "hostEmail": rows["hostEmail"],
                    "meeting": rows["meeting"]
                    }
                )

        # print(meetingDetails)
        return(meetingDetails)

def deleteMeetings(meetingsList):
    print("\nDeleting Zoom Meetings")
    meetingsReport = []
    payload = {}
    headers = {'authorization': ('Bearer ' + (bearer)),
                   'content-type': 'application/json'}

    for eachMeeting in meetingsList:
        url = ("https://api.zoom.us/v2/meetings/" + eachMeeting["meeting"] + "?schedule_for_reminder=false&cancel_meeting_reminder=false")
        response = requests.request("DELETE", url, headers=headers, data=payload)
        print("Deleting Meeting: " + eachMeeting["meeting"] + " for host " + eachMeeting["host"] + " " + str(response))
        meetingsReport.append(
            {
                "host": eachMeeting["host"],
                "meeting": eachMeeting["meeting"],
                "response": (response)
            })
    return(meetingsReport)


def saveMeetingsReportCSV(meetingsReport):
    fields = ["meeting", "host", "response"]
    try:
        with open("zoomResponse.csv", 'w', encoding='utf-8') as f:
            # Define the header row
            writer = csv.DictWriter(f, fieldnames=fields)
            # Write the header row
            writer.writeheader()
            # Fill in data rows
            writer.writerows(meetingsReport)
        print("Output File created.")
    except:
        print("*** Failed to write CSV output File. \n")

def main():

    # import meeting IDs from csv file into meetingsList array
    meetingsList = getCSV()
    meetingsReport = deleteMeetings(meetingsList)
    saveMeetingsReportCSV(meetingsReport)
   

if __name__ == "__main__":
    main()
