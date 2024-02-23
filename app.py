from flask import Flask, request, redirect, render_template, url_for, session, jsonify, send_file, flash
from db_manager import DBManager, DatabaseError, IntegrityError, OperationalError, SignupError
from apscheduler.schedulers.background import BackgroundScheduler
import time
import shutil
import os
import io
import base64
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'PLACEHOLDER'

db_manager = DBManager('partners.db')

# TODO: add exception handling, if user tries adding partner that already exists, tries changing partner name to already existing partner
# TODO: add more color to the ui
# TODO: add 25 examples


def backup_db():
    try:
        timestamp = time.strftime('%Y%m%d-%H%M%S')
        backup_filename = f'db_backup_{timestamp}.db'
        shutil.copyfile('partners.db', backup_filename)
    except Exception as e:
        print('Error making backup: ', e)

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
        except SignupError as e:
            return render_template('signup.html', error='The username already exists!')
        except DatabaseError as e:
            return render_template('signup.html', error='There was a problem connecting to the database. Please try again.')
        except Exception as e:
            return render_template('signup.html', error='An unexpected error occurred. Please try again.')
    else:
        return render_template('signup.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        try:
            valid_login, user_id = db_manager.verify_credentials(username, password)
            if valid_login:
                session['logged_in'] = True
                session['username'] = username
                session['user_id'] = user_id
                return redirect(url_for('main'))
            else:
                return render_template('login.html', error='Invalid username or password')
        except DatabaseError as e:
            return render_template('login.html', error='There was a problem connecting to the database. Please try again.')
        except Exception as e:
            return render_template('login.html', error='An unexpected error occurred. Please try again.')
    else:
        return render_template('login.html')


@app.route('/main')
def main():
    if 'logged_in' in session and session['logged_in']:
        search_query = request.args.get('searchQuery', None)
        try:
            if search_query:
                partners = db_manager.search_partners(search_query)
            else:
                partners = db_manager.get_all_partners(session['user_id'])
            return render_template('main.html', partners=partners, searchQuery=search_query)
        except DatabaseError as e:
            return render_template('main.html', error='An error occurred while connecting to the database. Please try again.')
        except Exception as e:
            return render_template('main.html', error='An error occurred while fetching partner data. Please try again.')
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
    phone = request.form.get('phone', '')
    bookmarked = False

    file = request.files.get('partner-image')
    if file and file.filename != '':
        image_data = file.read()
        image_mime_type = file.content_type
    else:
        image_data = None
        image_mime_type = None

    try:
        db_manager.add_partner(user_id, organization_name, type_of_organization, organization_is_other_type, resources_available, resources_available_is_other_type, description, contact_name, role, email, phone, bookmarked, image_data, image_mime_type)
    except IntegrityError:
        pass
    except OperationalError:
        pass
    except DatabaseError as e:
        return render_template('signup.html', error='There was a problem connecting to the database. Please try again.')
    return redirect(url_for('main'))


@app.route('/partner/modify/<int:partner_id>', methods=['POST'])
def modify_partner(partner_id):
    try:
        image = request.files.get('image')
        image_data = None
        image_mime_type = None
        if image:
            image_data = image.read()
            image_mime_type = image.content_type

        data = request.form
        db_manager.modify_partner(
            partner_id,
            organization_name=data.get('organization_name'),
            type_of_organization=data.get('partnerType'),
            organization_is_other_type=data.get('partnerTypeIsOther') == 'true',
            resources_available=data.get('resourcesAvailable'),
            resources_available_is_other_type=data.get('resourcesAvailableIsOtherType') == 'true',
            description=data.get('partnerDescription'),
            contact_name=data.get('contactName'),
            role=data.get('contactRole'),
            email=data.get('contactEmail'),
            phone=data.get('partnerTelephoneNumber'),
            bookmarked=data.get('bookmarked'),
            image_data=image_data,
            image_mime_type=image_mime_type
        )
        return jsonify({'success': True, 'message': 'successfully updated partner'}), 200
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500


@app.route('/partner/details/<int:partner_id>')
def partner_details(partner_id):
    try:
        partner_data = db_manager.get_partner_by_id(partner_id)
        if partner_data:
            partner_data = dict(list(partner_data.items())[:-2])
            return jsonify(partner_data)
        else:
            return jsonify({'error': 'Partner not found'}), 404
    except DatabaseError as e:
        return jsonify({'error': 'An error occurred while fetching partner data', 'details': str(e)}), 500


@app.route('/search')
def search():
    if 'logged_in' not in session or not session['logged_in']:
        return redirect(url_for('login'))
    
    search_query = request.args.get('searchQuery', '')
    types = request.args.getlist('types')
    resources = request.args.getlist('resources')

    partners = db_manager.search_partners(search_query, types, resources)
    return render_template('main.html', partners=partners, searchQuery=search_query)


@app.route('/toggle_bookmark/<int:partner_id>', methods=['POST'])
def toggle_bookmark(partner_id):
    try:
        partner = db_manager.get_partner_by_id(partner_id)
        if not partner:
            return render_template('main.html')

        new_status = not partner['Bookmarked']
        db_manager.modify_partner(partner_id, bookmarked=new_status)
        return redirect(url_for('main'))
    except Exception as e:
        return str(e), 500


@app.route('/partner-image/<int:partner_id>')
def partner_image(partner_id):
    print("Received request for partner image:", partner_id)
    image_data, image_mime_type = db_manager.get_partner_image(partner_id)
    if image_data and image_mime_type:
        return send_file(io.BytesIO(image_data), mimetype=image_mime_type)
    else:
        pass


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