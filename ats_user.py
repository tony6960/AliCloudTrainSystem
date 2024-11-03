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


class TempUser:
    def __init__(self, req_id, by):
        self.req_id = req_id
        self.login_by = by
        self.status = 'waiting'

    def create_new_user(self, name, score, user_class, cursor, conn):
        cursor.execute("INSERT INTO 'ats_user' ('username', 'password', 'group', 'class', 'score', 'status') VALUES (?, 'stu_123456', 'student', ?, ?, '0')", (name, user_class, score))
        conn.commit()
        self.status = 'done'
