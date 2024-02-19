from flask import Flask, request, redirect, render_template, url_for, flash
from db_manager import DBManager

app = Flask(__name__)
app.secret_key = 'J8489$ngo4ga89(*&HG#87h`p9T*($Whtp9uehfg)hgi&94hpw'

db_manager = DBManager('partners.db')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        input_password = request.form['password']
        if db_manager.verify_password(input_password):
            # return redirect(url_for('dashboard'))
            flash('good job')
            return render_template('index.html')
        else:
            flash('Invalid credentials, please try again.')
            return render_template('login.html')
    else:
        return render_template('login.html')

# @app.route('/add_partner', methods=['POST'])
# def add_partner():
#     data = request.json
#     db_manager.add_partner(data['organization_name'], data['type_of_organization'], data['resources_available'], data['description'])
#     return jsonify({'message': 'Partner added successfully'}), 201

# @app.route('/add_contact', methods=['POST'])
# def add_contact():
#     data = request.json
#     db_manager.add_contact(data['partner_id'], data['contact_name'], data['role'], data['email'], data['phone'])
#     return jsonify({'message': 'Contact added successfully'}), 201

# @app.route('/remove_partner/<int:partner_id>', methods=['DELETE'])
# def remove_partner(partner_id):
#     db_manager.remove_partner(partner_id)
#     return jsonify({'message': 'Partner removed successfully'}), 200

# @app.route('/remove_contact/<int:contact_id>', methods=['DELETE'])
# def remove_contact(contact_id):
#     db_manager.remove_contact(contact_id)
#     return jsonify({'message': 'Contact removed successfully'}), 200

# @app.route('/modify_partner/<int:partner_id>', methods=['PUT'])
# def modify_partner(partner_id):
#     data = request.json
#     db_manager.modify_partner(partner_id, **data)
#     return jsonify({'message': 'Partner modified successfully'}), 200

# @app.route('/modify_contact/<int:contact_id>', methods=['PUT'])
# def modify_contact(contact_id):
#     data = request.json
#     db_manager.modify_contact(contact_id, **data)
#     return jsonify({'message': 'Contact modified successfully'}), 200

# @app.route('/get_all_partners', methods=['GET'])
# def get_all_partners():
#     partners = db_manager.get_all_partners()
#     return jsonify(partners), 200

# @app.route('/get_all_contacts', methods=['GET'])
# def get_all_contacts():
#     contacts = db_manager.get_all_contacts()
#     return jsonify(contacts), 200

# @app.route('/set_password', methods=['POST'])
# def set_password():
#     data = request.json
#     db_manager.set_password(data['password'])
#     return jsonify({'message': 'Password set successfully'}), 200

# @app.route('/login', methods=['POST'])
# def login():
#     data = request.json
#     username = data.get('username')
#     input_password = data.get('password')
#     if db_manager.verify_password(input_password):
#         return jsonify({'message': 'Login successful'}), 200
#     else:
#         return jsonify({'error': 'Invalid credentials'}), 401
