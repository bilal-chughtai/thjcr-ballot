from flask_login import UserMixin
from app import login, db
import json
from datetime import datetime


# class User(UserMixin):
#     def __init__(self, crsid):
#         self.id = crsid
#         self.refresh()
#
#
#     def refresh(self):
#         with open("ballots/testballot/data/users.json", 'r') as all_user_data: TODO:remove hardcoding - use a settings file
#             self.user_data = json.load(all_user_data)[self.id]
#
#
#     def __repr__(self):
#         return '<User {}>'.format(self.crsid)


class User(UserMixin, db.Model):
    """
    Defines a user of the system
    1-1 with Ballot
    1-1 with Admins

    """
    id = db.Column(db.String, primary_key=True)
    first_name = db.Column(db.String, index=True)
    surname = db.Column(db.String, index=True)
    year = db.Column(db.Integer, index=True)
    #current_room = db.Column(db.String, index=True)
    ballot_slot = db.Column(db.DateTime, index=True)
    ballot_position = db.Column(db.Integer, index=True)
    ballot = db.relationship('Ballot', primaryjoin="User.id == Ballot.crsid", backref=db.backref("balloting_user", uselist=False))


class Ballot(db.Model):
    """
    Defines a ballot - a user choosing a room.
    1-1 with User
    1-1 with Room
    """
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    crsid = db.Column(db.String, db.ForeignKey('user.id'))
    room_id = db.Column(db.String, db.ForeignKey('room.id'))
    room = db.relationship('Room', primaryjoin="Ballot.room_id == Room.id", backref=db.backref("associated_ballot", uselist=False))


class Site(db.Model):
    """
    Defines a site in which a room may live
    1-Many with Room
    """
    id = db.Column(db.String, primary_key=True)
    site = db.Column(db.String)


class Room(db.Model):
    """
    Defines a room
    many-1 with Site
    """
    id = db.Column(db.String, primary_key=True)
    site_id = db.Column(db.Integer, db.ForeignKey('site.id'))
    site = db.relationship('Site', primaryjoin="Room.site_id == Site.id", backref="rooms")
    type = db.Column(db.String, index=True)
    floor = db.Column(db.Integer, index=True)
    notes = db.Column(db.String)
    taken_by = db.Column(db.String, db.ForeignKey('user.id'), index=True)
    weekly_rent = db.Column(db.Numeric, index=True)
    #TODO: add special properties eg large etc



class Admins(db.Model):
    """
    Defines admins of the system, with elevated privelages
    1-1 with user
    """
    id = db.Column(db.Integer, primary_key=True)
    crsid = db.Column(db.Integer, db.ForeignKey('user.id'))
    role = db.Column(db.String)
    user = db.relationship('User', primaryjoin="Admins.crsid==User.id", backref="admin")

@login.user_loader
def load_user(crsid):
    return User(crsid)
