from flask import flash, session
from app import redis, app
import traceback


USER_PREFIX = "user::"

class Credential:
    ''' class of credential methods '''
    def _create_credential(self, form):
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


    def _validate_credential(self, form):
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

credential = Credential()