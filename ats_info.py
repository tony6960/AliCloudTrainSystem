from ats_checker import *
import ast


def index_data_create(find_user, user_list, cursor):
    temp = {'score': 'error', 'group': 'error', 'class': 'error'}
    for user in user_list:
        if user.username == find_user:
            temp['score'] = user.get_score(cursor)
            temp['group'] = user.get_group(cursor)
            temp['class'] = user.get_class(cursor)
    return temp


def get_notice(token, user_list, cursor):
    temp = []
    cookie_check_result = cookie_checker(token, user_list)
    if cookie_check_result:
        cursor.execute("SELECT content,from_user from ats_notice where class=? OR class='all'", (cookie_check_result['obj'].get_class(cursor),))
        notice_back_result = cursor.fetchall()
        for notice in notice_back_result:
            temp.append({'content': notice[0] + '-' + notice[1]})
    else:
        temp.append({'content': 'ERROR'})
    return temp


def get_no_train(token, user_list, cursor):
    temp = []
    cookie_check_result = cookie_checker(token, user_list)
    if cookie_check_result:
        cursor.execute("SELECT name,list FROM ats_train where class=? OR class='all'", (cookie_check_result['obj'].get_class(cursor),))
        train_back_result = cursor.fetchall()
        for train in train_back_result:
            if cookie_check_result['name'] in ast.literal_eval(train[1])['nofinish']:
                temp.append({'content': train[0]})
    else:
        temp.append({'content': 'ERROR'})
    return temp
