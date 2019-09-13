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
    1-Many with Ballots
    1-Many with Reviews

    """
    id = db.Column(db.String, primary_key=True)
    first_name = db.Column(db.String, index=True)
    surname = db.Column(db.String, index=True)
    year = db.Column(db.Integer, index=True)
    ballot_slot = db.Column(db.DateTime, index=True)
    ballot_position = db.Column(db.Integer, index=True) #set to 0 if not balloting this year
    reviews = db.relationship('User', primaryjoin="User.id == Review.author_crsid", backref=db.backref("author"))
    ballots = db.relationship('Ballot', primaryjoin="Ballot.crsid == User.id", backref=db.backref("user"))


class Ballot(db.Model):
    """
    Defines a ballot - a user choosing a room.
    Many-1 with User
    Many-1 with Room

    """
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    crsid = db.Column(db.String, db.ForeignKey('user.id'))
    room_id = db.Column(db.String, db.ForeignKey('room.id'))
    for_year = db.Column(db.Integer, index=True) #balloting for which year




class Room(db.Model):
    """
    Defines a room
    many-1 with Site <-- to do
    1-many with Ballot - can backref Room.ballots.crsid order by timestamp where for_year = 2020 to get taken by info
    1-many with Image
    1-many with Review
    """
    id = db.Column(db.String, primary_key=True) #these should be the svg ids, a converter is found in gsheet_tools
    friendly_name = db.Column(db.String, index=True) # these are the normal names, eg BBC B10
    site = db.Column(db.String, index=True)
    type = db.Column(db.String, index=True)
    floor = db.Column(db.Integer, index=True)
    notes = db.Column(db.String)
    weekly_rent = db.Column(db.Numeric, index=True)
    images = db.relationship('Image', primaryjoin="Image.room_id == Room.id", backref=db.backref("room"))
    ballots = db.relationship('Ballot', primaryjoin="Ballot.room_id == Room.id", backref=db.backref("room"))
    reviews = db.relationship('Review', primaryjoin="Review.room_id == Room.id", backref=db.backref("room"))
    #TODO: add special properties eg large etc


class Review(db.Model):
    """
    Defines a review of a room
    many-1 with user
    many-1 with room
    1-many with image
    """
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    author_crsid = db.Column(db.String, db.ForeignKey('User.id'), index=True)
    room_id = db.Column(db.String, db.ForeignKey('Room.id'), index=True)
    text = db.Column(db.String)
    size = db.Column(db.Integer, index=True)
    noise = db.Column(db.Integer, index=True)
    value = db.Column(db.Integer, index=True)
    overall = db.Column(db.Integer, index=True)
    images = db.relationship('Image', primaryjoin="Review.id == Image.review_id", backref=db.backref("review"))


class Image(db.Model):
    """
    Defines an image, which may be added through a review
    many-1 with review
    many-1 with room
    """
    id = db.Column(db.Integer, primary_key=True)
    author_crsid = db.Column(db.String, db.ForeignKey('User.id'), index=True)
    room_id = db.Column(db.String, db.ForeignKey('room.id'), index=True)
    review_id = db.Column(db.Integer, db.ForeignKey('Review.id'), index=True) #set to 0 if independent of review
    filename = db.Column(db.String)


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
    return User.query.get(crsid)
