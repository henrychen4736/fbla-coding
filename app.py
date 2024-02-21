from flask import Flask, request, redirect, render_template, url_for, session, jsonify
from db_manager import DBManager, DatabaseError, IntegrityError, OperationalError, SignupError
from apscheduler.schedulers.background import BackgroundScheduler
import time
import shutil
import os

app = Flask(__name__)
app.secret_key = 'PLACEHOLDER'

db_manager = DBManager('partners.db')

# TODO: add exception handling
# TODO: add auto redirecting to signup page when going to index
# TODO: add more color to the ui
# TODO: add searching, filtering
# TODO: add 25 examples
# TODO: make help page better
# TODO: add button to clear search/filters
# TODO: new font
# TODO: make the 0 on the filter mean number of partners in that category
# TODO: generate report feature
# TODO: find some way to handle the "other type"


def backup_db():
    timestamp = time.strftime('%Y%m%d-%H%M%S')
    backup_filename = f'db_backup_{timestamp}.db'
    shutil.copyfile('partners.db', backup_filename)
    print(f'Backup created: {backup_filename}')

scheduler = BackgroundScheduler()
scheduler.add_job(func=backup_db, trigger='interval', weeks=1)
scheduler.start()


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
    if 'logged_in' in session and session['logged_in']:
        search_query = request.args.get('searchQuery', None)
        print('SESSION: ',session)
        if search_query:
            partners = db_manager.search_partners(search_query)
            print('Search query:' + search_query)
        else:
            partners = db_manager.get_all_partners(session['user_id'])
        print('PARTNERS: ',partners)
        return render_template('main.html', partners=partners, searchQuery=search_query)
    else:
        return redirect(url_for('login'))


@app.route('/add_partner', methods=['POST'])
def add_partner():
    if 'logged_in' not in session or not session['logged_in']:
        return redirect(url_for('login'))

    user_id = session['user_id']
    organization_name = request.form['organization_name']
    type_of_organization = request.form['type_of_organization']
    other_type = request.form.get('other_type', '')

    organization_is_other_type = (type_of_organization == 'Other')
    if organization_is_other_type:
        type_of_organization = other_type

    resources_available = request.form['resources_available']
    other_resource = request.form.get('other_resource', '')

    resources_available_is_other_type = (resources_available == 'Other')
    if resources_available_is_other_type:
        resources_available = other_resource

    description = request.form.get('description', '')
    contact_name = request.form.get('contact_name', '')
    role = request.form.get('role', '')
    email = request.form.get('email', '')
    phone = request.form.get('phone')
    bookmarked = False

    file = request.files.get('partner-image')
    if file and file.filename != '':
        image_data = file.read()
    else:
        image_data = None

    try:
        print('PARAMS FOR ADDING PARTNER:',user_id, organization_name, type_of_organization, organization_is_other_type, resources_available, resources_available_is_other_type, description, contact_name, role, email, phone, bookmarked)
        db_manager.add_partner(user_id, organization_name, type_of_organization, organization_is_other_type, resources_available, resources_available_is_other_type, description, contact_name, role, email, phone, bookmarked, image_data)
        print('partner added')
    except Exception as e:
        print("EXEPTION: ", e)

    return redirect(url_for('main'))


@app.route('/search', methods=['GET'])
def search():
    if 'logged_in' in session and session['logged_in']:
        search_query = request.args.get('searchQuery', '')
        search_results = db_manager.search_partners(search_query)
        print('SEARCH RESULTS: ',search_results)
        return render_template('main.html', partners=search_results, searchQuery=search_query)
    else:
        return redirect(url_for('login'))


@app.route('/toggle_bookmark/<int:partner_id>', methods=['POST'])
def toggle_bookmark(partner_id):
    try:
        partner = db_manager.get_partner_by_id(partner_id)
        if not partner:
            return render_template('main.html')
            print('PARTNER NOT FOUND')

        new_status = not partner['Bookmarked']
        db_manager.modify_partner(partner_id, bookmarked=new_status)
        return redirect(url_for('main'))
    except Exception as e:
        return str(e), 500


@app.route('/help')
def help():
    return render_template('help.html')


@app.route('/logout')
def logout():
    session['logged_in'] = False
    session.clear()
    return redirect(url_for('login'))


@app.route('/')
def index():
    return redirect(url_for('login'))