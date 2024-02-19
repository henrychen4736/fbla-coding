import sqlite3 as sql

# TODO: make it so methods don't need to access by ID, but with name instead
# TODO: add error handling
class DBManager:
    def __init__(self, db_name):
        self.db_name = db_name

    def _connect(self):
        return sql.connect(self.db_name)

    def add_partner(self, organization_name, type_of_organization, resources_available, description):
        conn = self._connect()
        c = conn.cursor()
        c.execute('''INSERT INTO Partners (OrganizationName, TypeOfOrganization, ResourcesAvailable, Description) VALUES (?, ?, ?, ?)''', (organization_name, type_of_organization, resources_available, description))
        conn.commit()
        conn.close()

    def add_contact(self, partner_id, contact_name, role, email, phone):
        conn = self._connect()
        c = conn.cursor()
        c.execute('''INSERT INTO Contacts (PartnerID, ContactName, Role, Email, Phone) VALUES (?, ?, ?, ?, ?)''', (partner_id, contact_name, role, email, phone))
        conn.commit()
        conn.close()

    def remove_partner(self, partner_id):
        conn = self._connect()
        c = conn.cursor()
        c.execute('DELETE FROM Contacts WHERE PartnerID = ?', (partner_id,))
        c.execute('DELETE FROM Partners WHERE ID = ?', (partner_id,))
        conn.commit()
        conn.close()

    def remove_contact(self, contact_id):
        conn = self._connect()
        c = conn.cursor()
        c.execute('DELETE FROM Contacts WHERE ID = ?', (contact_id,))
        conn.commit()
        conn.close()

    def modify_partner(self, partner_id, organization_name=None, type_of_organization=None, resources_available=None, description=None):
        conn = self._connect()
        c = conn.cursor()
        updates = []
        params = []
        if organization_name:
            updates.append('OrganizationName = ?')
            params.append(organization_name)
        if type_of_organization:
            updates.append('TypeOfOrganization = ?')
            params.append(type_of_organization)
        if resources_available:
            updates.append('ResourcesAvailable = ?')
            params.append(resources_available)
        if description:
            updates.append('Description = ?')
            params.append(description)
        params.append(partner_id)
        query = 'UPDATE Partners SET ' + ', '.join(updates) + ' WHERE ID = ?'
        c.execute(query, params)
        conn.commit()
        conn.close()

    def modify_contact(self, contact_id, contact_name=None, role=None, email=None, phone=None):
        conn = self._connect()
        c = conn.cursor()
        updates = []
        params = []
        if contact_name:
            updates.append('ContactName = ?')
            params.append(contact_name)
        if role:
            updates.append('Role = ?')
            params.append(role)
        if email:
            updates.append('Email = ?')
            params.append(email)
        if phone:
            updates.append('Phone = ?')
            params.append(phone)
        params.append(contact_id)
        query = 'UPDATE Contacts SET ' + ", ".join(updates) + ' WHERE ID = ?'
        c.execute(query, params)
        conn.commit()
        conn.close()

    def get_all_partners(self):
        conn = self._connect()
        c = conn.cursor()
        c.execute("SELECT * FROM Partners")
        partners = c.fetchall()
        conn.close()
        columns = ['ID', 'OrganizationName', 'TypeOfOrganization', 'ResourcesAvailable', 'Description']
        partners_list = []
        for partner in partners:
            partner_dict = dict(zip(columns, partner))
            partners_list.append(partner_dict)
        return partners_list

    def get_all_contacts(self):
        conn = self._connect()
        c = conn.cursor()
        c.execute("SELECT * FROM Contacts")
        contacts = c.fetchall()
        conn.close()
        columns = ['ID', 'PartnerID', 'ContactName', 'Role', 'Email', 'Phone']
        contacts_list = []
        for contact in contacts:
            contact_dict = dict(zip(columns, contact))
            contacts_list.append(contact_dict)
        return contacts_list
    
    def set_password(self, password):
        conn = self._connect()
        c = conn.cursor()
        c.execute('DELETE FROM AdminAuth')
        c.execute('INSERT INTO AdminAuth (password) VALUES (?)', (password,))
        conn.commit()
        conn.close()