from flask_login import UserMixin
from app import login
import json


class User(UserMixin):
    def __init__(self, crsid):
        self.id = crsid
        self.refresh()


    def refresh(self):
        with open("ballots/testballot/data/users.json", 'r') as all_user_data: #TODO:remove hardcoding - use a settings file
            self.user_data = json.load(all_user_data)[self.id]





    def __repr__(self):
        return '<User {}>'.format(self.crsid)


@login.user_loader
def load_user(crsid):
    return User(crsid)
