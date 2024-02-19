import sqlite3 as sql
from db_manager import DBManager
import os

def setup(name):
   conn = sql.connect(name)
   c = conn.cursor()

   c.execute(
      '''CREATE TABLE IF NOT EXISTS Partners (
         ID INTEGER PRIMARY KEY,
         OrganizationName TEXT NOT NULL UNIQUE,
         TypeOfOrganization TEXT,
         ResourcesAvailable TEXT,
         Description TEXT
      )'''
   )

   c.execute(
      '''CREATE TABLE IF NOT EXISTS Contacts (
         ID INTEGER PRIMARY KEY,
         PartnerID INTEGER,
         ContactName TEXT NOT NULL,
         Role TEXT,
         Email TEXT,
         Phone TEXT,
         FOREIGN KEY (PartnerID) REFERENCES Partners(ID)
         UNIQUE(PartnerID, ContactName)
      )'''
   )

   c.execute(
      '''CREATE TABLE IF NOT EXISTS AdminAuth (
         username TEXT NOT NULL,
         password TEXT NOT NULL
      )'''
   )

   # TODO: make it so the user can set a password and username, and also add password encryption
   c.execute('INSERT INTO AdminAuth (username, password) VALUES (?, ?)', ('123456', '123'))

   conn.commit()
   conn.close()

def test_db(name):
   os.remove(name)
   setup(name)
   db_man = DBManager(name)

   db_man.add_partner("FBLA", "club", None, "future business leaders of america")
   db_man.add_partner("HOSA", "club", None, "hosa")
   db_man.add_contact(1, "joe", "president", "joe@gmail.com", 626123123123)
   db_man.add_contact(1, "bob", "vice president", "bob@gmail.com", 123)
   db_man.add_contact(2, "bobby", "president", "bobby@gmail.com", 123123123123)
   db_man.modify_contact(1, "john", None, None, None)
   db_man.modify_partner(1, "code club", "club", None, "CODING")
   db_man.remove_contact(1)
   db_man.remove_partner(1)
   partners_list = db_man.get_all_partners()
   print(partners_list)
   contacts_list = db_man.get_all_contacts()
   print(contacts_list)
   db_man.set_password("123")

setup("partners.db")
# test_db("partners.db")