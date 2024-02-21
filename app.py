from flask import Flask, request, redirect, render_template, url_for, flash
from db_manager import DBManager

app = Flask(__name__)
app.secret_key = 'J8489$ngo4ga89(*&HG#87h`p9T*($Whtp9uehfg)hgi&94hpw'

db_manager = DBManager('partners.db')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if db_manager.verify_credentials(username, password):
            return redirect(url_for('main'))
        else:
            return render_template('login.html')
    else:
        return render_template('login.html')

@app.route('/main')
def main():
    contacts = {
        'Contact 1': 'Description for Contact 1',
        'Contact 2': 'Description for Contact 2',
        'Contact 3': 'Description for Contact 3',
        'Contact 4': 'Description for Contact 4',
    }
    return render_template('main.html', contacts=contacts)