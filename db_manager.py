import sqlite3 as sql
import bcrypt


class DatabaseError(Exception):
    pass


class IntegrityError(DatabaseError):
    pass


class OperationalError(DatabaseError):
    pass


class SignupError(DatabaseError):
    pass

'''
A class with several methods to add/modify records in the database
'''
class DBManager:
    def __init__(self, db_name):
        self.db_name = db_name

    '''
    A private method used to connect to the database. Helps avoid repitition of the database file name and
    includes error handling.
    '''
    def _connect(self):
        try:
            return sql.connect(self.db_name)
        except sql.Error as e:
            logger.error(f'An error occurred connecting to the database: {e}')
            raise DatabaseError(f'An error occurred connecting to the database: {e}')

    '''
    A private method used to execute a query on the database. Improves error handling by wrapping it in 
    one function.
    '''
    def _execute(self, cursor, query, params=()):
        try:
            cursor.execute(query, params)
        except sql.IntegrityError as e:
            logger.error(f'Integrity error: {e}')
            raise IntegrityError(f'Integrity error: {e}')
        except sql.OperationalError as e:
            logger.error(f'Operational error: {e}')
            raise OperationalError(f'Operational error: {e}')
        except sql.Error as e:
            logger.error(f'Database error: {e}')
            raise DatabaseError(f'Database error: {e}')

    '''
    method to add a partner to the database
    '''
    def add_partner(self, user_id, organization_name, type_of_organization, organization_is_other_type, resources_available, resources_available_is_other_type, description, contact_name, role, email, phone, bookmarked, image_data=None, image_mime_type='png'):
        if image_data is None:
            with open('./static/assets/company-placeholder.png', 'rb') as default_image:
                image_data = default_image.read()
        try:
            conn = self._connect()
            c = conn.cursor()
            self._execute(c, 'INSERT INTO Partners (UserID, OrganizationName, TypeOfOrganization, OrganizationIsOtherType, ResourcesAvailable, ResourcesAvailableIsOtherType, Description, ContactName, Role, Email, Phone, Bookmarked, ImageData, ImageMimeType) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
                          (user_id, organization_name, type_of_organization, organization_is_other_type, resources_available, resources_available_is_other_type, description, contact_name, role, email, phone, bookmarked, image_data, image_mime_type))
            conn.commit()
        except Exception:
            raise
        finally:
            conn.close()

    '''
    method to remove a partner from the database
    '''
    def remove_partner(self, partner_id):
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

    '''
    method to modify a partner using the id.
    '''
    def modify_partner(self, partner_id, organization_name=None, type_of_organization=None, organization_is_other_type=None, resources_available=None, resources_available_is_other_type=None, description=None, contact_name=None, role=None, email=None, phone=None, bookmarked=None, image_data=None, image_mime_type=None):
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

    '''
    method to fetch information about one partner using ID
    '''
    def get_partner_by_id(self, partner_id):
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

    '''
    method to get all the partners of a user
    '''
    def get_all_partners(self, user_id):
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
    
    '''
    method to return the image of a partner by ID
    '''
    def get_partner_image(self, partner_id):
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

    '''
    method that returns partners by searching and filtering. It takes a keyword, and two optional
    filters: the type of partner and the resources of the partner
    '''
    def search_partners(self, search_query, types=None, resources=None):
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
        except Exception as e:
            raise
        finally:
            conn.close()

    '''
    method to add a new user using a username and password. Raises a SignupError if a username is already
    taken. Encrypts password with bcrypt
    '''
    def register_user(self, username, password):
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

    '''
    method to allow a user to log in. Passwords are safely stored using bcrypt.
    '''
    def verify_credentials(self, input_username, input_password):
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
