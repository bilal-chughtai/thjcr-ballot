from app import app
from flask import render_template,flash,redirect, url_for, session, request
from app.forms import LoginForm
from flask_raven import raven_auth

@app.route('/')
@app.route('/index')
def index():
    if '_raven' in session:
        user = {'username': session['_raven']}
    else:
        user= {'username': "please log in"}
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
    return render_template('index.html', title='Home', user=user, posts=posts)

@app.route('/login', methods=['GET', 'POST'])
#@raven_auth()
def login():

    x,y = raven_auth(session,request)

    print(y)

    session['_raven'] = y

    return redirect(x)

    # form = LoginForm()
    # if form.validate_on_submit():
    #     flash('Login requested for user {}, remember_me={}'.format(
    #         form.username.data, form.remember_me.data))
    #     return redirect(url_for('index'))
    # return render_template('login.html', title='Sign In', form=form)

@app.errorhandler(400)
def urlparser(s):
    print(session['_raven'])
    if session['_raven'] is None or session['_raven'] =='':
        x, y = raven_auth(session, request)

        print(y)

        session['_raven'] = y

        return redirect(x)
    else:
        return redirect("/index")