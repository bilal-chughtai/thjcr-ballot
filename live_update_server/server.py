#! /usr/bin/python

import argparse
from datetime import datetime
import time
import os
import json

from utils import NonRepeatingLogger
from googlesheet import GoogleSheetReader
# TODO decide better file naming for the following three
from roomdataparser import RoomDataParser
from roomdataformatter import RoomDataFormatter
from nametosvgid import RoomNameToSvgId

parser = argparse.ArgumentParser(description='Provide live updates for an instance of the THJCR ballot')
parser.add_argument("--ballot-directory", required=True, help="Path to currently active ballot where this script has write permissions", type=str)
parser.add_argument("--google-sheet-name", required=True, help="Name of the single sheet on the Google doc to read updates from", type=str)
parser.add_argument("--sheet-format", required=True, help="Path to JSON file that defines the mapping of columns when reading document updates", type=str)
parser.add_argument("--google-API-credentials", required=True, help="Path to JSON file with the Google Drive API secret that authorizes access to the sheet provided", type=str)
parser.add_argument("--room-svg-id-to-room-name", required=True, help="Path to CSV file mapping SVG file room id to the name used in the Google Sheet", type=str)
parser.add_argument("--google-doc-title", required=True, help="Exact name of the google doc to link the ballot site to.")

args = parser.parse_args()

# validate given ballot directory is valid
# TODO

# validate can access google sheet with the credentials provided
# TODO


# server logfile for this ballot
logfile = "server_log_{0}.log".format(args.google_sheet_name)
logger = NonRepeatingLogger(logfile, sort_by_most_recent=False)


sheet_columns_format = json.load(open(args.sheet_format))['sheet_columns_mapping']

room_name_to_svg_id = RoomNameToSvgId(args.room_svg_id_to_room_name)

sheet_reader = GoogleSheetReader(args.google_API_credentials)
doc_title = args.google_doc_title
sheet_name = args.google_sheet_name
sheet = sheet_reader.get_sheet(doc_title, sheet_name)
rooms = RoomDataParser(sheet, sheet_columns_format, room_name_to_svg_id.names_to_ids(), logger)

try:
    os.mkdir(os.path.join(args.ballot_directory, "data"))
except OSError:
     #directory already exists
    pass
output_file_path = os.path.join(args.ballot_directory, "data", "data.json")

while True:
    # parse the sheet to into a local data format
    sheet = sheet_reader.get_sheet(doc_title, sheet_name)
    new_rooms = RoomDataParser(sheet, sheet_columns_format, room_name_to_svg_id.names_to_ids(), logger)

    print("Polling sheet")

    # see if it's different from what we parsed before
    if new_rooms != rooms:
        print("--changed detected")
        # if so, save it
        rooms = new_rooms
        # convert local data format into JSON to send over write to file
        json_room_data = RoomDataFormatter.build_rooms_json(rooms)
        # overwrite the JSON data file
        with open(output_file_path, 'w') as outfile:
            json.dumps(json_room_data, outfile)
    # sleep to not poll too often
    time.sleep(5)