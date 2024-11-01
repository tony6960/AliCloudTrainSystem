class User:
    def __init__(self, username, token):
        self.username = username
        self.token = token

    def get_score(self, cursor):
        cursor.execute('SELECT score FROM ats_user where username=?', (self.username,))
        result = cursor.fetchone()
        return result[0]

    def get_group(self, cursor):
        cursor.execute('SELECT "group" FROM ats_user where username=?', (self.username,))
        result = cursor.fetchone()
        return result[0]

    def get_class(self, cursor):
        cursor.execute('SELECT class FROM ats_user where username=?', (self.username,))
        result = cursor.fetchone()
        return result[0]
