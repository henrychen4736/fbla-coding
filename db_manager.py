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


class DBManager:
    def __init__(self, db_name):
        self.db_name = db_name

    def _connect(self):
        try:
            return sql.connect(self.db_name)
        except sql.Error as e:
            raise Exception(
                f'An error occurred connecting to the database: {e}')

    def _execute(self, cursor, query, params=()):
        try:
            cursor.execute(query, params)
        except sql.IntegrityError as e:
            raise IntegrityError(f'Integrity error: {e}')
        except sql.OperationalError as e:
            raise OperationalError(f'Operational error: {e}')
        except sql.Error as e:
            raise DatabaseError(f'Database error: {e}')

    def add_partner(self, user_id, organization_name, type_of_organization, resources_available, description, contact_name, role, email, phone):
        try:
            conn = self._connect()
            c = conn.cursor()
            self._execute(c, 'INSERT INTO Partners (UserID, OrganizationName, TypeOfOrganization, ResourcesAvailable, Description, ContactName, Role, Email, Phone) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)',
                          (user_id, organization_name, type_of_organization, resources_available, description, contact_name, role, email, phone))
            conn.commit()
        except Exception:
            raise
        finally:
            conn.close()

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

    def modify_partner(self, partner_id, organization_name=None, type_of_organization=None, resources_available=None, description=None, contact_name=None, role=None, email=None, phone=None):
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
            if resources_available is not None:
                updates.append('ResourcesAvailable = ?')
                params.append(resources_available)
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

    def get_all_partners(self, user_id):
        try:
            conn = self._connect()
            c = conn.cursor()
            self._execute(
                c, 'SELECT ID, OrganizationName, TypeOfOrganization, ResourcesAvailable, Description, ContactName, Role, Email, Phone FROM Partners WHERE UserID = ?', (user_id,))
            partners = c.fetchall()
            columns = ['ID', 'OrganizationName', 'TypeOfOrganization',
                       'ResourcesAvailable', 'Description', 'ContactName', 'Role', 'Email', 'Phone']
            partners_list = []
            for partner in partners:
                partner_dict = dict(zip(columns, partner))
                partners_list.append(partner_dict)
            return partners_list
        except Exception:
            raise
        finally:
            conn.close()

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
        except Exception:
            raise
        finally:
            conn.close()

    def verify_credentials(self, input_username, input_password):
        try:
            conn = self._connect()
            c = conn.cursor()
            self._execute(
                c, 'SELECT username, password FROM AdminAuth WHERE username = ?', (input_username,))
            user = c.fetchone()
            if user:
                stored_username, stored_password = user
                return bcrypt.checkpw(input_password.encode('utf-8'), stored_password)
            else:
                return False
        except Exception:
            raise
        finally:
            conn.close()
