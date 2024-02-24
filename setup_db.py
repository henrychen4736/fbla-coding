import sqlite3 as sql
from db_manager import DBManager
import os

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
            TypeOfOrganization TEXT NOT NULL,
            OrganizationIsOtherType BOOLEAN NOT NULL DEFAULT FALSE,
            ResourcesAvailable TEXT NOT NULL,
            ResourcesAvailableIsOtherType BOOLEAN NOT NULL DEFAULT FALSE,
            Description TEXT,
            ContactName TEXT NOT NULL,
            Role TEXT,
            Email TEXT NOT NULL,
            Phone TEXT NOT NULL,
            Bookmarked BOOLEAN NOT NULL DEFAULT FALSE,
            ImageData BLOB NOT NULL,
            ImageMimeType TEXT NOT NULL,
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

   organizations = [
      ('Apple Inc.', 'Technology', 'Innovative technology products, software, and services', 'Leading in consumer electronics and technology.'),
      ('Microsoft Corporation', 'Technology', 'Software, cloud computing, and related services', 'Pioneering in software development and cloud services.'),
      ('Amazon.com Inc.', 'Consumer Discretionary', 'E-commerce, cloud computing', 'Global leader in e-commerce and cloud computing.'),
      ('Facebook, Inc. (Meta Platforms, Inc.)', 'Communication Services', 'Social media and digital platforms', 'Connecting people through social media and technology.'),
      ('Alphabet Inc. (Google)', 'Communication Services', 'Search engine, digital advertising, and cloud services', 'Dominating digital search and online advertising.'),
      ('Berkshire Hathaway Inc.', 'Financials', 'Diversified investments, insurance, and other businesses', 'Holding company led by Warren Buffett with a diverse portfolio.'),
      ('Johnson & Johnson', 'Health Care', 'Pharmaceuticals, medical devices, and consumer health products', 'Leading in healthcare and consumer health products.'),
      ('Visa Inc.', 'Information Technology', 'Payment technology and services', 'Facilitating global electronic funds transfers.'),
      ('Procter & Gamble Co.', 'Consumer Staples', 'Consumer goods including health and beauty products', 'Manufacturing a wide range of consumer goods.'),
      ('JPMorgan Chase & Co.', 'Financials', 'Banking and financial services', 'Leading global financial services firm.'),
      ('UnitedHealth Group Incorporated', 'Health Care', 'Healthcare products and insurance services', 'Diversified healthcare company offering insurance and care.'),
      ('Intel Corporation', 'Technology', 'Semiconductors and microprocessors', 'Leading in semiconductor manufacturing.'),
      ('Verizon Communications Inc.', 'Communication Services', 'Wireless services and telecommunications', 'Major provider of telecommunications and wireless services.'),
      ('Coca-Cola Company', 'Consumer Staples', 'Beverage manufacturing and marketing', 'Iconic global beverage company.'),
      ('Pfizer Inc.', 'Health Care', 'Pharmaceuticals and biopharmaceuticals', 'Leading in drug development and healthcare.'),
      ('NVIDIA Corporation', 'Technology', 'Graphics processors and computing technology', 'Innovating in graphics and artificial intelligence computing.'),
      ('Walmart Inc.', 'Consumer Discretionary', 'Retail and wholesale operations', "World's largest retailer by revenue."),
      ('Home Depot, Inc.', 'Consumer Discretionary', 'Home improvement retail', 'Leading home improvement retailer.'),
      ('Boeing Company', 'Industrials', 'Aerospace, defense, and space technology', 'Major manufacturer of commercial jets, defense, and space technology.'),
      ('Goldman Sachs Group, Inc.', 'Financials', 'Investment banking, financial management', 'Leading global investment banking and financial management firm.'),
      ('3M Company', 'Industrials', 'Diverse range of products and solutions across multiple sectors', 'Innovating in products for health care, safety, and more.'),
      ('Cisco Systems, Inc.', 'Technology', 'Networking hardware and telecommunications equipment', 'Leading in networking and communications technology.'),
      ('PepsiCo, Inc.', 'Consumer Staples', 'Food, snack, and beverage company', 'Competing in the global food and beverage industry.'),
      ('American Express Company', 'Financials', 'Credit card services and financial services', 'Providing global financial services and payment solutions.'),
      ("McDonald's Corporation", 'Consumer Discretionary', 'Global chain of fast food restaurants', "One of the world's leading fast-food chains."),
   ]


   for idx, (name, type, resources, description) in enumerate(organizations, start=1):
       email = f'contact{idx}@{name.replace(" ", "").lower()}.com'
       phone = f'555-00{idx:02}'
       db_manager.add_partner(1, name, type, True, resources, True, description, 'Contact Person', 'Outreach Coordinator', email, phone, False)


setup('partners.db') 
test_db('partners.db')