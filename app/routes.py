from app import app
from flask import render_template,flash,redirect, url_for, session, request
from app.forms import BallotForm
from flask_raven import raven_auth, raven_request
from flask_login import current_user, login_user, login_required
from app.models import User
import json

@app.route('/')

def index():
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    else:
        return render_template('welcome.html', title='Home')

@app.route('/home')
@login_required
def home():
    return render_template('home.html', name=current_user.first_name + ' ' + current_user.surname,
                           position=str(current_user.ballot_position), ballot_slot=current_user.ballot_slot,
                           crsid=current_user.id)



def check_crsid_valid(request): #TODO maybe move this function elsewhere, remove hardcoding of ballot
    crsid = raven_auth(request)
    print(crsid)
    user = User.query.filter_by(id=crsid).first()
    if user is not None:
        login_user(user)
        return url_for('index')
    else:
        return url_for('invalid_user', crsid=crsid)

@app.route('/invalid_user')
def invalid_user():
    return render_template('invalid_user.html', crsid=request.args['crsid'])


@app.route('/login', methods=['GET'])
def login():

    if "WLS-Response" in request.url:
        return redirect(check_crsid_valid(request))
    elif current_user.is_authenticated:
        return redirect(url_for('index'))
    else:
        return redirect(raven_request())

@app.route('/submit_ballot', methods=['GET', 'POST'])
def submit_ballot():

    # the idea is you cant access this page until your slot - hence loading in data and passing it to the form for
    # displaying / validation should be ok>??? TODO

    form = BallotForm()
    if form.validate_on_submit():
        #check ballot is valid
        flash('Ballot processed')
        return redirect(url_for("home"))
    return render_template('submit_ballot.html', title='Submit Ballot', form=form)

    # form = LoginForm()
    # if form.validate_on_submit():
    #     user = User.query.filter_by(username=form.username.data).first()
    #     if user is None or not user.check_password(form.password.data):
    #         flash('Invalid username or password')
    #         return redirect(url_for('login'))
    #     login_user(user, remember=form.remember_me.data)
    #     return redirect(url_for('index'))
    # return render_template('submit_ballot.html', title='Sign In', form=form)