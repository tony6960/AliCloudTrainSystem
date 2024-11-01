import uuid
from ats_user import *


def user_login_checker(user, passwd, cursor):
    cursor.execute('SELECT password from ats_user where username=?', (user,))
    result = cursor.fetchone()
    if result[0] == passwd:
        token = uuid.uuid4().hex
        return {'user': User(user, token), 'token': token}
    else:
        return False


def cookie_checker(token, user_list):
    for user in user_list:
        if user.token == token:
            return {'obj': user, 'name': user.username}
    return {'obj': False, 'name': False}
