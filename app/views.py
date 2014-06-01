from flask import Blueprint, render_template, request, flash, url_for, redirect, session
from app.decorators import login_required
from app.lib.credential import credential
from app import app
import sys


###############################################################################
# Instantiation
###############################################################################
main = Blueprint('app', __name__, template_folder='templates', static_folder='static')


###############################################################################
# Views
###############################################################################
@main.route('/', methods=['GET', 'POST'])
def front():
    if request.method == 'GET':
        return render_template('front.html')
    else:
        success, next_view = credential._validate_credential(request.form)
        return redirect(url_for('.' + next_view))
        # TODO: rate limit to 3 tries, then lock for 1hr, redirect to forgot password page


@main.route('/menu/')
def menu():
    return render_template('menu.html')


@main.route('/deck/')
def choose_deck():
    return 


@main.route('/deck/create/')
def create_deck():
    return 


@main.route('/deck/count/')
def count_deck():
    return 


@main.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'GET':
        return render_template('signup.html')
    else:
        success = credential._create_credential(request.form)
        if success:
            return redirect(url_for('.menu'))
        else:
            return redirect(url_for('.signup'))
