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


def temp_user_req_id_checker(req_id, temp_user_list):
    for user in temp_user_list:
        if user.req_id == req_id:
            return user
    return False


def cookie_checker(token, user_list):
    for user in user_list:
        if user.token == token:
            return {'obj': user, 'name': user.username}
    return {'obj': False, 'name': False}


def user_is_existence_checker(username, cursor):
    cursor.excute("SELECT username from ats_user where username=?", (username,))
    result = cursor.fetchone()
    if result:
        return True
    return False
