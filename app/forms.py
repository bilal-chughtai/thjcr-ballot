from flask_wtf import FlaskForm
from flask_login import current_user
from flask import request
from wtforms import StringField, PasswordField, BooleanField, SubmitField, HiddenField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.validators import DataRequired
from app.models import Ballot, User, Room
from app import db
import datetime


class BallotForm(FlaskForm):

    crsid = HiddenField()
    #ReadonlyStringField('CRSid', default=request.current_user.id)
    #room_name = StringField('Room', validators=[DataRequired()])
    room_name = QuerySelectField('Room', validators=[DataRequired()],
                                 query_factory = Room.query.all, get_pk=lambda x: x.id, get_label="friendly_name")

    for_year = StringField('For Year', validators=[DataRequired()])
    license = StringField('Licence', validators=[DataRequired()])
    submit = SubmitField('Submit')

    def validate(self):
        print(self.room_name.data)
        #validates the ballot is allowed
        #we only display valid rooms theoretically
        regular_validate = FlaskForm.validate(self)
        if not regular_validate:
            return False

        #TODO: check no other ballots by user


        #check user is in ballot slot
        ballot_slot = User.query.get(self.crsid.data).ballot_slot
        if not ballot_slot < datetime.datetime.utcnow() < ballot_slot+datetime.timedelta(seconds=600): #TODO remove hardcoding
            self.room_name.errors.append("It is not your time to ballot")
            return False



        # checks room hasn't been taken
        # converts the friendly name to the id used in the database before querying the ballot table
        ballots_for_room = Ballot.query.filter_by(room_id=Room.query.filter_by(friendly_name=self.room_name.data).first().id).all()
        print(ballots_for_room)
        for ballot in ballots_for_room:
            if ballot.for_year == int(self.for_year.data):
                self.room_name.errors.append('Room ' + self.room_name.data + ' for year ' + self.for_year.data + ' has been taken by ' + ballot.crsid)
                print("s")
                return False

        return True


