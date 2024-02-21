import sqlite3 as sql
from db_manager import DBManager
import os
import bcrypt

def setup(name):
   conn = sql.connect(name)
   c = conn.cursor()

   c.execute(
      '''CREATE TABLE IF NOT EXISTS Partners (
         ID INTEGER PRIMARY KEY,
         UserID INTEGER NOT NULL,
         OrganizationName TEXT NOT NULL,
         TypeOfOrganization TEXT,
         ResourcesAvailable TEXT,
         Description TEXT,
         FOREIGN KEY (UserID) REFERENCES AdminAuth(ID)
         UNIQUE(UserID, OrganizationName)
      )'''
   )

   c.execute(
      '''CREATE TABLE IF NOT EXISTS Contacts (
         ID INTEGER PRIMARY KEY,
         PartnerID INTEGER NOT NULL,
         ContactName TEXT NOT NULL,
         Role TEXT,
         Email TEXT,
         Phone TEXT,
         FOREIGN KEY (PartnerID) REFERENCES Partners(ID),
         UNIQUE(PartnerID, ContactName)
      )'''
   )

   c.execute(
      '''CREATE TABLE IF NOT EXISTS AdminAuth (
         ID INTEGER PRIMARY KEY,
         username TEXT NOT NULL UNIQUE,
         password TEXT NOT NULL
      )'''
   )

   pw = '123'
   hashed_pw = bcrypt.hashpw(pw.encode('utf-8'), bcrypt.gensalt())
   c.execute('INSERT INTO AdminAuth (username, password) VALUES (?, ?)', ('123456', hashed_pw))

   conn.commit()
   conn.close()

def test_db(name):
   os.remove(name)
   setup(name)
   db_man = DBManager(name)

   db_man.add_partner(1, 'FBLA', 'club', None, 'future business leaders of america')
   db_man.add_partner(1, 'HOSA', 'club', None, 'hosa')
   db_man.register_user('doggo', '345')
   db_man.add_contact(1, 'joe', 'president', 'joe@gmail.com', 626123123123)
   db_man.add_contact(2, 'joe', 'vice president', 'bob@gmail.com', 123)
   db_man.add_contact(2, 'bobby', 'president', 'bobby@gmail.com', 123123123123)
   db_man.modify_contact(1, 'john', None, None, None)
   db_man.modify_partner(1, 'code club', 'club', None, 'CODING')
   db_man.remove_contact(1)
   db_man.remove_partner(1)

# setup('partners.db')
test_db('partners.db')