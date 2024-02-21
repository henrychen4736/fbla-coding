import sqlite3 as sql
from db_manager import DBManager
import os
import bcrypt

def setup(name):
   if os.path.exists(name):
      os.remove(name)
   conn = sql.connect(name)
   c = conn.cursor()

   c.execute('''
        CREATE TABLE IF NOT EXISTS Partners (
            ID INTEGER PRIMARY KEY,
            UserID INTEGER NOT NULL,
            OrganizationName TEXT NOT NULL,
            TypeOfOrganization TEXT,
            ResourcesAvailable TEXT,
            Description TEXT,
            ContactName TEXT NOT NULL,
            Role TEXT,
            Email TEXT,
            Phone TEXT,
            FOREIGN KEY (UserID) REFERENCES AdminAuth(ID),
            UNIQUE(UserID, OrganizationName)
        )'''
    )

   c.execute(
      '''CREATE TABLE IF NOT EXISTS AdminAuth (
         ID INTEGER PRIMARY KEY,
         username TEXT NOT NULL UNIQUE,
         password TEXT NOT NULL
      )'''
   )

   conn.commit()
   conn.close()

def test_db(name):
   db_manager = DBManager(name)

   db_manager.register_user('user1', 'password1')
   db_manager.register_user('user2', 'password2')
   
   db_manager.add_partner(1, 'Company1', 'Type1', 'Resource1', 'Description1', 'Contact1', 'Role1', 'contact1@company1.com', '555-0001')
   db_manager.add_partner(1, 'Company2', 'Type2', 'Resource2', 'Description2', 'Contact2', 'Role2', 'contact2@company2.com', '555-0002')
   db_manager.add_partner(2, 'Company3', 'Type3', 'Resource3', 'Description3', 'Contact3', 'Role3', 'contact3@company3.com', '555-0003')
   db_manager.modify_partner(1, contact_name='Updated Contact1', email='updated1@company1.com')
   # db_manager.remove_partner(2)


setup('partners.db')
test_db('partners.db')