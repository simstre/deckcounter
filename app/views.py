from flask import Blueprint, render_template, request, flash, url_for, redirect, session
from datetime import datetime, date, timedelta
from app.decorators import login_required
from dateutil import parser
from app import redis, app
import requests
import traceback
import sys


###############################################################################
# Instantiation
###############################################################################
main = Blueprint('app', __name__, template_folder='templates', static_folder='static')

###############################################################################
# Constant
###############################################################################
USER_PREFIX = "user::"


###############################################################################
# View
###############################################################################
@main.route('/', methods=['GET', 'POST'])
def front():
    if request.method == 'GET':
        return render_template('front.html')
    else:
        success, next_view = _validate_credential(request.form)
        return redirect(url_for('.' + next_view))
        # TODO: rate limit to 3 tries, then lock for 1hr, redirect to forgot password page


@main.route('/menu')
@login_required
def menu():
    return render_template('menu.html')


@main.route('/create/deck')
@login_required
def create_deck():
    return 


@main.route('/count/deck')
@login_required
def count_deck():
    return 


@main.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'GET':
        return render_template('signup.html')
    else:
        success = _create_credential(request.form)
        if success:
            return redirect(url_for('.menu'))
        else:
            return redirect(url_for('.signup'))

###############################################################################
# Helper function
###############################################################################
def _create_credential(form):
    req = ['username', 'password']
    for field in req:
        if not form.get(field):
            flash("Missing " + field)
            return False
    username = form.get('username')
    password = form.get('password')
    email = form.get('email', None)

    exist = redis.hexists(USER_PREFIX + username, "password")
    if exist:
        flash("Username already in use")
        return False
    redis.hset(USER_PREFIX + username, "password", password)
    if email:
        redis.hset(USER_PREFIX + username, "email", email)
    session['username'] = username
    return True


def _validate_credential(form):
    req = ['username', 'password']
    for field in req:
        if not form.get(field):
            flash("Forgot to enter your " + field + "?")
            return False, 'front'
    username = form['username']
    password = form['password']

    #try:
        #redis.get("redis-app22172284")
#        except requests.ConnectionError:
#            app.logger.error("Unable to connect to Redis, username: " + username)
#            return redirect(url_for('error', error="Server unavailable"))
#        except Exception:
#            app.logger.warning(traceback.format_exc() + "username: " + username)
#            return redirect(url_for('error', error="Server unavailable"))

    correct_password = redis.hget(USER_PREFIX + username, "password")
    
    # Checks if the user is in the DB
    if correct_password is not None:
        # Password validation
        if password == correct_password:
            session['username'] = username
            return True, 'menu'
        else:
            flash("Invalid credential, try again")
            return False, 'front'
    else:
        # redirect user to sign up for us
        return False, 'signup'
