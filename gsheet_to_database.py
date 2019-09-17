#this should live in create ballot

# ! /usr/bin/python

import argparse
import time
import os
import json

from app.gsheet_tools.utils import NonRepeatingLogger
from app.gsheet_tools.googlesheet import GoogleSheetReader
# TODO decide better file naming for the following three
from app.gsheet_tools.roomdataparser import GoogleRoomDataParser, DummyRoomDataParser
from app.gsheet_tools.roomdataformatter import RoomDataFormatter
from app.gsheet_tools.nametosvgid import RoomNameToSvgId
from app.gsheet_tools.userdataparser import UserDataParser
from app.models import User, Ballot, Room, Admins
from app import db
import json
from datetime import datetime

# from .utils import NonRepeatingLogger
# from .googlesheet import GoogleSheetReader
# from .roomdataparser import RoomDataParser
# from .roomdataformatter import RoomDataFormatter
# from .nametosvgid import RoomNameToSvgId

parser = argparse.ArgumentParser(description='Provide live updates for an instance of the THJCR ballot')
parser.add_argument("--ballot-directory", required=True,
                    help="Path to currently active ballot where this script has write permissions", type=str)
parser.add_argument("--google-API-credentials", required=True,
                    help="Path to JSON file with the Google Drive API secret that authorizes access to the sheet provided",
                    type=str)
parser.add_argument("--google-doc-title", required=True,
                    help="Exact name of the google doc to link the ballot site to.")

parser.add_argument("--google-sheet-name", required=True,
                    help="Name of the single sheet on the Google doc to read updates from", type=str)
parser.add_argument("--google-sheet-format", required=True,
                    help="Path to JSON file that defines the mapping of columns when reading document updates",
                    type=str)
parser.add_argument("--room-svg-id-mapping", required=True,
                    help="Path to CSV file mapping SVG file room id to the name used in the Google Sheet", type=str)
parser.add_argument("--user-sheet-name", required=True,
                    help="Name of the google sheet mapping containing all system data", type=str)

args = parser.parse_args()

# validate given ballot directory is valid
# TODO

# validate can access google sheet with the credentials provided
# TODO

#gsheet format
rooms_sheet_columns_format = json.load(open(args.google_sheet_format))['room_sheet_columns_mapping']
users_sheet_columns_format = json.load(open(args.google_sheet_format))['users_sheet_columns_mapping']

#mapping of friendly room names to database/svg ids
room_name_to_svg_id = RoomNameToSvgId(args.room_svg_id_mapping)


sheet_reader = GoogleSheetReader(args.google_API_credentials)
doc_title = args.google_doc_title
room_sheet_name = args.google_sheet_name
users_sheet_name = args.user_sheet_name
room_sheet = sheet_reader.get_sheet(doc_title, room_sheet_name)
users_sheet = sheet_reader.get_sheet(doc_title, users_sheet_name)

try:
    os.mkdir(os.path.join(args.ballot_directory, "data"))
except OSError:
    # directory already exists
    pass

data_file_path = os.path.join(args.ballot_directory, "data", "data.json")
user_file_path = os.path.join(args.ballot_directory, "data", "users.json")


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
user_data = {}


print("Polling sheet")

# parse the data sheet into a local data format
users_sheet = sheet_reader.get_sheet(doc_title, users_sheet_name)
new_user_data_object = UserDataParser(users_sheet, users_sheet_columns_format, logger)
new_user_data = new_user_data_object._parsed_users

# parse the rooms sheet to into a local data format
room_sheet = sheet_reader.get_sheet(doc_title, room_sheet_name)
new_rooms = GoogleRoomDataParser(room_sheet, rooms_sheet_columns_format, room_name_to_svg_id.names_to_ids(), logger)

jsondumprawdata = new_rooms.get_parsed_rooms()

with open('rawdata.json', 'w') as outfile:
    json.dump(jsondumprawdata, outfile)




with open('rawdata.json') as file:
    room_data=json.load(file)

new_rooms=[]

#create a room model for each room in the json TODO: make this update or add
db_rooms = db.session.query(Room.id)
for id,room in room_data.items():
    if id in db_rooms:
        updated_room = Room.query.get(id)
        updated_room.update(id=key, friendly_name=room['roomName'], site=room['roomName'].split()[0], type=room['roomType'], floor=room['floor'], notes=room['notes'], weekly_rent=room['weeklyRent'])
    else:
        new_rooms.append(Room(id=key, friendly_name=room['roomName'], site=room['roomName'].split()[0], type=room['roomType'], floor=room['floor'], notes=room['notes'], weekly_rent=room['weeklyRent']))
db.session.bulk_save_objects(new_rooms)
db.session.commit()

with open('userdata.json') as file:
    user_data = json.load(file)

new_users=[]
db_users = db.session.query(User.id)
for id,user in user_data.items():
    slot = datetime.strptime(user['date'] + ' ' + user['time'], '%d/%m/%Y %H:%M')
    if id in db_users:
        updated_user = User.query.get(id)
        updated_user.update(id=key, first_name=user['name'], surname=user['surname'], year=int(user['year']), ballot_slot=slot, ballot_position=int(user['position']))
    else:
        new_users.append(User(id=key, first_name=user['name'], surname=user['surname'], year=int(user['year']), ballot_slot=slot, ballot_position=int(user['position'])))
db.session.bulk_save_objects(new_users)
db.session.commit()

#TODO: current room