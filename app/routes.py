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
        user = {'username': current_user.id}
    else:
        return render_template('welcome.html', title='Home')

@app.route('/home')
@login_required
def home():
    current_user.refresh()
    return render_template('home.html', user_data=current_user.user_data, crsid=current_user.id)



# @app.route('/login', methods=['GET', 'POST'])
# #@raven_auth()
# def login():
#
#     x,y = raven_auth(session,request)
#
#     print(y)
#
#     session['_raven'] = y
#
#     return redirect(x)

    # form = LoginForm()
    # if form.validate_on_submit():
    #     flash('Login requested for user {}, remember_me={}'.format(
    #         form.username.data, form.remember_me.data))
    #     return redirect(url_for('index'))
    # return render_template('submit_ballot.html', title='Sign In', form=form)

#@app.errorhandler(400) #hacky fix for redirect post raven log in button
def check_crsid_valid(request): #TODO maybe move this function elsewhere, remove hardcoding of ballot
    crsid = raven_auth(request)
    print(crsid)
    with open('ballots/testballot/data/users.json','r') as users:
        user_list = json.load(users)
    if crsid in user_list.keys():
        user = User(crsid)
        login_user(user)
        return url_for('index')
    else:
        return url_for('invalid_user', crsid=crsid)



@app.route('/invalid_user')
def invalid_user():
    return render_template('invalid_user.html', crsid=request.args['crsid'])


       # return redirect(x)
  #  else:
     #   return redirect("/index")

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
    form = BallotForm()
    if form.validate_on_submit():
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