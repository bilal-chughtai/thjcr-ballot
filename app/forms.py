from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired


class BallotForm(FlaskForm):
    roomName = StringField('Room', validators=[DataRequired()])
    license = StringField('Licence', validators=[DataRequired()])
    submit = SubmitField('Submit')