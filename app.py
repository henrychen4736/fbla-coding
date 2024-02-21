from flask import Flask, request, redirect, render_template, url_for, session, flash
from db_manager import DBManager, DatabaseError, IntegrityError, OperationalError, SignupError

app = Flask(__name__)
app.secret_key = 'PLACEHOLDER'
app.config['SESSION_PERMANENT'] = False

db_manager = DBManager('partners.db')

# TODO: add exception handling
# TODO: add auto redirecting to signup page when going to index
# TODO: add more color to the ui
# TODO: add searching, filtering
# TODO: add 25 examples
# TODO: add bookmarking system
# TODO: make help page better
# TODO: add navigations
# TODO: new font



@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        try:
            username = request.form['username']
            password = request.form['password']
            user_id = db_manager.register_user(username, password)
            session['logged_in'] = True
            session['username'] = username
            session['user_id'] = user_id
            return redirect(url_for('main'))
        except SignupError:
            return render_template('signup.html', error='The username already exists!')
    else:
        return render_template('signup.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        valid_login, user_id = db_manager.verify_credentials(username, password)
        if valid_login:
            session['logged_in'] = True
            session['username'] = username
            session['user_id'] = user_id
            return redirect(url_for('main'))
        else:
            return render_template('login.html', error='Invalid username or password')
    else:
        return render_template('login.html')


@app.route('/main')
def main():
    print(session)
    if 'logged_in' in session and session['logged_in']:
        partners = db_manager.get_all_partners(session['user_id'])
        return render_template('main.html', partners=partners)
    else:
        return redirect(url_for('login'))


@app.route('/help')
def help():
    return render_template('help.html')


@app.route('/logout')
def logout():
    session.clear()
    print(session)
    flash('You have successfully logged out.', 'info')
    return redirect(url_for('login'))