#this should live in create ballot

from app.models import User, Ballot, Room, Admins
from app import db
import json

with open('rawdata.json') as file:
    room_data=json.load(file)

rooms=[]

#create a room model for each room in the json
for key,room in room_data.items():
    rooms.append(Room(id=key, friendly_name=room['roomName'], site=room['roomName'].split()[0], type=room['roomType'], floor=room['floor'], notes=room['notes'], weekly_rent=room['weeklyRent']))

db.session.bulk_save_objects(rooms)
db.session.commit()