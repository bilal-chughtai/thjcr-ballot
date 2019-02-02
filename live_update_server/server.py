#! /usr/bin/python

import argparse
from datetime import datetime
import time
import os
import json

from live_update_server.utils import NonRepeatingLogger
from live_update_server.googlesheet import GoogleSheetReader
# TODO decide better file naming for the following three
from live_update_server.roomdataparser import GoogleRoomDataParser,DummyRoomDataParser
from live_update_server.roomdataformatter import RoomDataFormatter
from live_update_server.nametosvgid import RoomNameToSvgId
# from .utils import NonRepeatingLogger
# from .googlesheet import GoogleSheetReader
# from .roomdataparser import RoomDataParser
# from .roomdataformatter import RoomDataFormatter
# from .nametosvgid import RoomNameToSvgId

parser = argparse.ArgumentParser(description='Provide live updates for an instance of the THJCR ballot')
parser.add_argument("--ballot-directory", required=True, help="Path to currently active ballot where this script has write permissions", type=str)
parser.add_argument("--google-API-credentials", required=True, help="Path to JSON file with the Google Drive API secret that authorizes access to the sheet provided", type=str)
parser.add_argument("--google-doc-title", required=True, help="Exact name of the google doc to link the ballot site to.")

parser.add_argument("--google-sheet-name", required=True, help="Name of the single sheet on the Google doc to read updates from", type=str)
parser.add_argument("--google-sheet-format", required=True, help="Path to JSON file that defines the mapping of columns when reading document updates", type=str)
parser.add_argument("--room-svg-id-mapping", required=True, help="Path to CSV file mapping SVG file room id to the name used in the Google Sheet", type=str)

args = parser.parse_args()

# validate given ballot directory is valid
# TODO

# validate can access google sheet with the credentials provided
# TODO


# server logfile for this ballot
logfile = "server_log_{0}.log".format(args.google_sheet_name)
logger = NonRepeatingLogger(logfile, sort_by_most_recent=False)


sheet_columns_format = json.load(open(args.google_sheet_format))['sheet_columns_mapping']

room_name_to_svg_id = RoomNameToSvgId(args.room_svg_id_mapping)

sheet_reader = GoogleSheetReader(args.google_API_credentials)
doc_title = args.google_doc_title
sheet_name = args.google_sheet_name
sheet = sheet_reader.get_sheet(doc_title, sheet_name)

try:
    os.mkdir(os.path.join(args.ballot_directory, "data"))
except OSError:
     #directory already exists
    pass
output_file_path = os.path.join(args.ballot_directory, "data", "data.json")


# fun add on functionality to maintain order of updates bar
def put_updated_rooms_timestamps(new_rooms, old_rooms):
    """ Does an in place modification to add timestampe attr. Just uses a local time rather than proper API """
    # find all rooms that are different
    attr = "lastUpdated"
    new_data, old_data = new_rooms.get_parsed_rooms(), old_rooms.get_parsed_rooms()
    for room_id in new_data:
        new_room = new_data[room_id]
        if room_id not in old_data or new_room['surname'].strip() != old_data[room_id]['surname'].strip():
            new_rooms.add_attribute(room_id, attr, time.time())

rooms = DummyRoomDataParser()
while True:
    print("Polling sheet")
    
    # parse the sheet to into a local data format
    sheet = sheet_reader.get_sheet(doc_title, sheet_name)
    new_rooms = GoogleRoomDataParser(sheet, sheet_columns_format, room_name_to_svg_id.names_to_ids(), logger)

    # see if it's different from what we parsed before
    if new_rooms != rooms:
        print("--changed detected")
        # if so, save it
        put_updated_rooms_timestamps(new_rooms, rooms)
        rooms = new_rooms
        # convert local data format into JSON to send over write to file
        json_room_data = RoomDataFormatter.build_rooms_json(rooms)
        # overwrite the JSON data file
        with open(output_file_path, 'w') as outfile:
            print("Writing new data file {0}".format(output_file_path))
            json.dump(json_room_data, outfile)
    
    # since this is only 1 connection, we can poll often
    time.sleep(3)