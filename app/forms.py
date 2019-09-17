from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired
from app.models import Ballot, User, Room


class BallotForm(FlaskForm):
    room_name = StringField('Room', validators=[DataRequired()])
    for_year = StringField('For Year')
    license = StringField('Licence', validators=[DataRequired()])
    submit = SubmitField('Submit')

    def validate(self):
        rv = FlaskForm.validate(self)
        if not rv:
            return False

        # checks room hasn't been taken
        ballots_for_room = Ballot.query.filter_by(room_id=Room.query.filter_by(friendly_name=self.room_name.data).first())
        for ballot in ballots_for_room:
            if ballot.for_year == self.for_year.data:
                self.room_name.errors.append('Room ' + self.room_name.data + ' for year ' + self.for_year.data + ' has been taken by ' + ballot.crsid)
                return False

        return True