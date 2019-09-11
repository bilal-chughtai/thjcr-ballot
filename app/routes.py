from app import app
from flask import render_template,flash,redirect, url_for, session, request
from app.forms import LoginForm
from flask_raven import raven_auth, raven_request
from flask_login import current_user, login_user, login_required
from app.models import User
import json

@app.route('/')
@app.route('/')
def index():
    if current_user.is_authenticated:
        user = {'username': current_user.id}
    else:
        user = {'username': "please log in"}
    posts = [
        {
            'author': {'username': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'username': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        }
    ]
    return render_template('index.html', title='Home', user=user)

@app.route('/home')
@login_required
def home():
    current_user.refresh()
    return render_template('home.html', user_data=current_user.user_data, crsid=current_user.id)

@app.route('/home')


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
    # return render_template('login.html', title='Sign In', form=form)

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



    # form = LoginForm()
    # if form.validate_on_submit():
    #     user = User.query.filter_by(username=form.username.data).first()
    #     if user is None or not user.check_password(form.password.data):
    #         flash('Invalid username or password')
    #         return redirect(url_for('login'))
    #     login_user(user, remember=form.remember_me.data)
    #     return redirect(url_for('index'))
    # return render_template('login.html', title='Sign In', form=form)