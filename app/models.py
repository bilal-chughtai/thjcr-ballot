from flask_login import UserMixin
from app import login

class User(UserMixin):
    def __init__(self, CRSid):
        self.CRSid = CRSid
        #TODO: add more fields here read in through data dict - persists while loaded easiest


    def __repr__(self):
        return '<User {}>'.format(self.CRSid)


@login.user_loader
def load_user(CRSid):
    return User(CRSid)
