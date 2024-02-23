import sqlite3 as sql
import bcrypt
import xlsxwriter
from io import BytesIO


class DatabaseError(Exception):
    pass


class IntegrityError(DatabaseError):
    pass


class SignupError(DatabaseError):
    pass

'''
A class with several methods to add/modify records in the database
'''
class DBManager:
    def __init__(self, db_name):
        self.db_name = db_name

    def _connect(self):
        '''
        A private method used to connect to the database. Helps avoid repitition of the database file name and
        includes error handling.
        
        Returns:
            sqlite3.Connection: A connection object to the database.
        
        Raises:
            DatabaseError: If there is an error connecting to the database.
        '''
        try:
            return sql.connect(self.db_name)
        except sql.Error as e:
            raise DatabaseError(f'An error occurred connecting to the database: {e}')

    def _execute(self, cursor, query, params=()):
        '''
        A private method used to execute a query on the database. Improves error handling by wrapping it in 
        one function.

        Args:
            cursor (sqlite3.Cursor): The cursor object to execute the query.
            query (str): The SQL query to execute.
            params (tuple, optional): The parameters to pass into the query.

        Raises:
            IntegrityError: If there is an integrity error in the database.
            DatabaseError: If there is a generic database error.
        '''
        try:
            cursor.execute(query, params)
        except sql.IntegrityError as e:
            raise IntegrityError(f'Integrity error: {e}')
        except sql.Error as e:
            raise DatabaseError(f'Database error: {e}')

    def add_partner(self, user_id, organization_name, type_of_organization, organization_is_other_type, resources_available, resources_available_is_other_type, description, contact_name, role, email, phone, bookmarked, image_data=None, image_mime_type=None):
        '''
        method to add a partner to the database
        '''
        if image_data is None:
            with open('./static/assets/company-placeholder.png', 'rb') as default_image:
                image_data = default_image.read()
                image_mime_type = 'png'
        try:
            conn = self._connect()
            c = conn.cursor()
            self._execute(c, 'INSERT INTO Partners (UserID, OrganizationName, TypeOfOrganization, OrganizationIsOtherType, ResourcesAvailable, ResourcesAvailableIsOtherType, Description, ContactName, Role, Email, Phone, Bookmarked, ImageData, ImageMimeType) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
                          (user_id, organization_name, type_of_organization, organization_is_other_type, resources_available, resources_available_is_other_type, description, contact_name, role, email, phone, bookmarked, image_data, image_mime_type))
            conn.commit()
        except Exception as e:
            print(e)
            raise
        finally:
            conn.close()

    def remove_partner(self, partner_id):
        '''
        method to remove a partner from the database
        '''
        try:
            conn = self._connect()
            c = conn.cursor()
            self._execute(
                c, 'DELETE FROM Partners WHERE ID = ?', (partner_id,))
            conn.commit()
        except Exception:
            raise
        finally:
            conn.close()

    def modify_partner(self, partner_id, organization_name=None, type_of_organization=None, organization_is_other_type=None, resources_available=None, resources_available_is_other_type=None, description=None, contact_name=None, role=None, email=None, phone=None, bookmarked=None, image_data=None, image_mime_type=None):
        '''
        method to modify a partner using the id.
        '''
        try:
            conn = self._connect()
            c = conn.cursor()
            updates = []
            params = []

            if organization_name is not None:
                updates.append('OrganizationName = ?')
                params.append(organization_name)
            if type_of_organization is not None:
                updates.append('TypeOfOrganization = ?')
                params.append(type_of_organization)
            if organization_is_other_type is not None:
                updates.append('OrganizationIsOtherType = ?')
                params.append(organization_is_other_type)
            if resources_available is not None:
                updates.append('ResourcesAvailable = ?')
                params.append(resources_available)
            if resources_available_is_other_type is not None:
                updates.append('ResourcesAvailableIsOtherType = ?')
                params.append(resources_available_is_other_type)
            if description is not None:
                updates.append('Description = ?')
                params.append(description)
            if contact_name is not None:
                updates.append('ContactName = ?')
                params.append(contact_name)
            if role is not None:
                updates.append('Role = ?')
                params.append(role)
            if email is not None:
                updates.append('Email = ?')
                params.append(email)
            if phone is not None:
                updates.append('Phone = ?')
                params.append(phone)
            if bookmarked is not None:
                updates.append('Bookmarked = ?')
                params.append(bookmarked)
            if image_data is not None:
                updates.append('ImageData = ?')
                params.append(image_data)
            if image_mime_type is not None:
                updates.append('ImageMimeType = ?')
                params.append(image_mime_type)

            if updates:
                params.append(partner_id)
                query = 'UPDATE Partners SET ' + \
                    ', '.join(updates) + ' WHERE ID = ?'
                self._execute(c, query, params)
                conn.commit()
        except Exception:
            raise
        finally:
            conn.close()

    def get_partner_by_id(self, partner_id):
        '''
        method to fetch information about one partner using ID
        '''
        try:
            conn = self._connect()
            c = conn.cursor()
            self._execute(c, 'SELECT ID, OrganizationName, TypeOfOrganization, OrganizationIsOtherType, ResourcesAvailable, ResourcesAvailableIsOtherType, Description, ContactName, Role, Email, Phone, Bookmarked, ImageData, ImageMimeType FROM Partners WHERE ID = ?', (partner_id,))
            partner = c.fetchone()
            if partner:
                columns = ['ID', 'OrganizationName', 'TypeOfOrganization', 'OrganizationIsOtherType', 'ResourcesAvailable', 'ResourcesAvailableIsOtherType', 'Description', 'ContactName', 'Role', 'Email', 'Phone', 'Bookmarked', 'ImageData', 'ImageMimeType']
                partner_dict = dict(zip(columns, partner))
                return partner_dict
            else:
                return None
        except Exception:
            raise
        finally:
            conn.close()

    def get_all_partners(self, user_id):
        '''
        method to get all the partners of a user
        '''
        try:
            conn = self._connect()
            c = conn.cursor()
            self._execute(
                c, 'SELECT ID, OrganizationName, TypeOfOrganization, OrganizationIsOtherType, ResourcesAvailable, ResourcesAvailableIsOtherType, Description, ContactName, Role, Email, Phone, Bookmarked, ImageData, ImageMimeType FROM Partners WHERE UserID = ? ORDER BY Bookmarked DESC, OrganizationName ASC', (user_id,))
            partners = c.fetchall()
            columns = ['ID', 'OrganizationName', 'TypeOfOrganization', 'OrganizationIsOtherType', 'ResourcesAvailable', 'ResourcesAvailableIsOtherType', 'Description', 'ContactName', 'Role', 'Email', 'Phone', 'Bookmarked', 'ImageData', 'ImageMimeType']
            partners_list = []
            for partner in partners:
                partner_dict = dict(zip(columns, partner))
                partners_list.append(partner_dict)
            return partners_list
        except Exception:
            raise
        finally:
            conn.close()
    
    def get_partner_image(self, partner_id):
        '''
        method to return the image of a partner by ID
        '''
        conn = self._connect()
        c = conn.cursor()
        try:
            c.execute('SELECT ImageData, ImageMimeType FROM Partners WHERE ID = ?', (partner_id,))
            row = c.fetchone()
            if row:
                return row
        finally:
            conn.close()
        return None, None

    def search_partners(self, search_query, types=None, resources=None):
        '''
        method that returns partners by searching and filtering. It takes a keyword, and two optional
        filters: the type of partner and the resources of the partner
        '''
        try:
            conn = self._connect()
            c = conn.cursor()
            search_pattern = f'%{search_query}%'
            query_parts = [
                'SELECT ID, OrganizationName, TypeOfOrganization, OrganizationIsOtherType, ResourcesAvailable, ResourcesAvailableIsOtherType, Description, ContactName, Role, Email, Phone, Bookmarked, ImageData, ImageMimeType FROM Partners WHERE (OrganizationName LIKE ? OR ContactName LIKE ? OR Description LIKE ?)'
            ]
            params = [search_pattern, search_pattern, search_pattern]

            if types:
                if 'Other' in types:
                    types.remove('Other')
                    query_parts.append('AND (OrganizationIsOtherType = 1)')
                else:
                    query_parts.append('AND TypeOfOrganization IN ({})'.format(','.join(['?']*len(types))))
                    params.extend(types)

            if resources:
                if 'Other' in resources:
                    resources.remove('Other')
                    query_parts.append('AND (ResourcesAvailableIsOtherType = 1)')
                else:
                    query_parts.append('AND ResourcesAvailable IN ({})'.format(','.join(['?']*len(resources))))
                    params.extend(resources)

            query = ' '.join(query_parts)
            self._execute(c, query, params)
            partners = c.fetchall()

            columns = ['ID', 'OrganizationName', 'TypeOfOrganization', 'OrganizationIsOtherType', 'ResourcesAvailable', 'ResourcesAvailableIsOtherType', 'Description', 'ContactName', 'Role', 'Email', 'Phone', 'Bookmarked', 'ImageData', 'ImageMimeType']
            partners_list = []
            for partner in partners:
                partner_dict = dict(zip(columns, partner))
                partners_list.append(partner_dict)
            return partners_list
        except Exception:
            raise
        finally:
            conn.close()
    
    def generate_excel(self, optional_columns):
        '''
        Generates an Excel file in memory containing data from the Partners table,
        based on a list of optional columns to include alongside the organization name.
        The Excel file is generated with xlsxwriter and stored in a BytesIO object
        to avoid saving to disk
        '''
        try:
            columns = ['OrganizationName'] + optional_columns
            conn = self._connect()
            cursor = conn.cursor()
            query = f"SELECT {', '.join(columns)} FROM Partners"
            self._execute(cursor, query)
            data = cursor.fetchall()
            conn.close()

            output = BytesIO()
            workbook = xlsxwriter.Workbook(output, {'in_memory': True})
            worksheet = workbook.add_worksheet()

            for col_num, header in enumerate(columns):
                worksheet.write(0, col_num, header)
            
            for row_num, row_data in enumerate(data, 1):
                for col_num, cell_data in enumerate(row_data):
                    worksheet.write(row_num, col_num, cell_data)
            
            workbook.close()

            output.seek(0)
            return output
        except Exception:
            raise
        finally:
            conn.close()


    def register_user(self, username, password):
        '''
        method to add a new user using a username and password. Raises a SignupError if a username is already
        taken. Encrypts password with bcrypt
        '''
        try:
            conn = self._connect()
            c = conn.cursor()
            self._execute(
                c, 'SELECT * FROM AdminAuth WHERE username = ?', (username,))
            if c.fetchone():
                raise SignupError('Username is already taken')

            hashed_password = bcrypt.hashpw(
                password.encode('utf-8'), bcrypt.gensalt())
            self._execute(
                c, 'INSERT INTO AdminAuth (username, password) VALUES (?, ?)', (username, hashed_password))
            conn.commit()
            user_id = c.lastrowid
            return user_id
        except Exception:
            raise
        finally:
            conn.close()

    def verify_credentials(self, input_username, input_password):
        '''
        method to allow a user to log in. Passwords are safely stored using bcrypt.
        '''
        try:
            conn = self._connect()
            c = conn.cursor()
            self._execute(
                c, 'SELECT ID, username, password FROM AdminAuth WHERE username = ?', (input_username,))
            user = c.fetchone()
            if user:
                user_id, stored_username, stored_password = user
                if bcrypt.checkpw(input_password.encode('utf-8'), stored_password):
                    return True, user_id
                else:
                    return False, None
            else:
                return False, None
        except Exception:
            raise
        finally:
            conn.close()
