from app import app, db
from app.models import User, Ballot, Site, Room, Admins

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Ballot': Ballot, 'Site': Site, 'Room': Room, 'Admins': Admins}