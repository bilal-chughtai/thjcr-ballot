#this should live in create ballot

from app.models import User, Ballot, Room, Admins
from app import db
import json
from datetime import datetime

with open('rawdata.json') as file:
    room_data=json.load(file)

rooms=[]

#create a room model for each room in the json TODO: make this update or add
for key,room in room_data.items():

    rooms.append(Room(id=key, friendly_name=room['roomName'], site=room['roomName'].split()[0], type=room['roomType'], floor=room['floor'], notes=room['notes'], weekly_rent=room['weeklyRent']))

#db.session.bulk_save_objects(rooms)
#db.session.commit()

with open('userdata.json') as file:
    user_data=json.load(file)

users=[]
for key,user in user_data.items():
    slot=datetime.strptime(user['date']+' '+user['time'], '%d/%m/%Y %H:%M')

    users.append(User(id=key, first_name=user['name'], surname=user['surname'], year=int(user['year']), ballot_slot=slot, ballot_position=int(user['position'])))
 #TODO: current room
#db.session.bulk_save_objects(users)
#db.session.commit()