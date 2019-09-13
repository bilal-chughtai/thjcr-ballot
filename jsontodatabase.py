#this should live in create ballot

from app.models import User, Ballot, Room, Admins
from app import db
import json
from datetime import datetime

with open('rawdata.json') as file:
    room_data=json.load(file)

new_rooms=[]

#create a room model for each room in the json TODO: make this update or add
db_rooms = db.session.query(Room.id)
for id,room in room_data.items():
    if id in db_rooms:
        updated_room = Room.query.filter_by(id=id).first()
        updated_room.update(id=key, friendly_name=room['roomName'], site=room['roomName'].split()[0], type=room['roomType'], floor=room['floor'], notes=room['notes'], weekly_rent=room['weeklyRent'])
    else:
        new_rooms.append(Room(id=key, friendly_name=room['roomName'], site=room['roomName'].split()[0], type=room['roomType'], floor=room['floor'], notes=room['notes'], weekly_rent=room['weeklyRent']))
db.session.bulk_save_objects(new_rooms)
db.session.commit()

with open('userdata.json') as file:
    user_data=json.load(file)

new_users=[]
db_users = db.session.query(User.id)
for id,user in user_data.items():
    slot = datetime.strptime(user['date'] + ' ' + user['time'], '%d/%m/%Y %H:%M')
    if id in db_users:
        updated_user = User.query.filter_by(id=id).first()
        updated_user.update(id=key, first_name=user['name'], surname=user['surname'], year=int(user['year']), ballot_slot=slot, ballot_position=int(user['position']))
    else:
        new_users.append(User(id=key, first_name=user['name'], surname=user['surname'], year=int(user['year']), ballot_slot=slot, ballot_position=int(user['position'])))
db.session.bulk_save_objects(new_rooms)
db.session.commit()




 #TODO: current room
#db.session.bulk_save_objects(users)
#db.session.commit()