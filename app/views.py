from flask import Blueprint, render_template, request, flash, url_for, redirect, session
from app.decorators import login_required
from app.lib.credential import credential
from app import app
import sys, os, jinja2, json
from settings import APP_STATIC


###############################################################################
# Instantiation
###############################################################################
main = Blueprint('app', __name__, template_folder='templates', static_folder='static')
app.jinja_env.add_extension('jinja2.ext.do')


###############################################################################
# Views
###############################################################################
@main.route('/', methods=['GET', 'POST'])
def front():
    if request.method == 'GET':
        if session.get('username'):
            return redirect(url_for('.menu'))
        return render_template('front.html')
    else:
        success, next_view = credential._validate_credential(request.form)
        return redirect(url_for('.' + next_view))
        # TODO: rate limit to 3 tries, then lock for 1hr, redirect to forgot password page


@main.route('/menu')
def menu():
    if session.get('username'):
        return render_template('menu.html', session=1)
    return render_template('menu.html', session=0)


@main.route('/deck/count')
def count_deck():
    return render_template('count_deck.html')


@main.route('/deck')
def choose_deck():
    if session.get('username'):
        # TODO: check if the user has any deck saved, if so, display a thumbnail for each deck
        return render_template('choose_deck.html', decks=[])
    else:
        return render_template('choose_deck.html', decks=[])


@main.route('/deck/create')
def create_deck():
    active = request.args.get('active')
    view = request.args.get('view')
    category = request.args.get('category')

    with open(os.path.join(APP_STATIC, 'data/cards.json')) as f:
        cards = f.read()
    data = json.loads(cards)
    return render_template('create_deck.html', active=active, view=view, category=category, data=data['cards'])




@main.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'GET':
        if session.get('username'):
            return redirect(url_for('.menu'))
        return render_template('signup.html')
    else:
        success = credential._create_credential(request.form)
        if success:
            return redirect(url_for('.menu'))
        else:
            return redirect(url_for('.signup'))
