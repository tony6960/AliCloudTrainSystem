from flask import Flask, request, render_template, make_response, redirect, url_for, g, jsonify
import sqlite3
from ats_checker import *
from ats_info import *
import uuid

app = Flask(__name__)
conn = sqlite3.connect('ATS.db', check_same_thread=False)
cursor = conn.cursor()
user_list = []
temp_user_list = []


@app.before_request
def create_req_id():
    g.req_id = str(uuid.uuid4().hex)


@app.route('/')
def index():
    token = request.cookies.get('token')
    if not token:
        return redirect(url_for('login'))
    cookie_check_result = cookie_checker(token, user_list)['name']
    if cookie_check_result:
        return render_template('index.html', user=cookie_check_result, data=index_data_create(cookie_check_result, user_list, cursor))
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        login_by = request.args.get('by')
        if login_by == 'bcczcs':
            response = make_response(redirect(f'https://bcczcs.com/api/v1/login?from=ats&req={g.req_id}'))
            temp_user_list.append(TempUser(g.req_id, 'bcczcs'))
            return response
        return render_template('login.html')
    else:
        username = request.form.get('username')
        password = request.form.get('password')
        login_check_result = user_login_checker(username, password, cursor)
        if login_check_result:
            user_list.append(login_check_result['user'])
            response = make_response(redirect(url_for('index')))
            response.set_cookie('token', login_check_result['token'])
            return response
        else:
            return '账户或密码错误,<a href="/login">返回上一步</a>'


@app.route('/api/v1/notice')
def api_v1_notice():
    token = request.cookies.get('token')
    return get_notice(token, user_list, cursor)


@app.route('/api/v1/no_train')
def api_v1_no_train():
    token = request.cookies.get('token')
    return get_no_train(token, user_list, cursor)


@app.route('/api/v1/login_back')
def api_v1_login_back():
    req_id = request.form.get('req')
    name = request.form.get('name')
    score = request.form.get('score')
    user_class = request.form.get('class')
    user = temp_user_req_id_checker(req_id, temp_user_list)
    if user:
        if user_is_existence_checker(name, cursor):
            token = uuid.uuid4().hex
            user_list.append(User(name, token))
            response = {'token': token, 'user': name}
            return jsonify(response)
        user.create_new_user(name, int(score), user_class, cursor, conn)
        token = uuid.uuid4().hex
        user_list.append(User(name, token))
        response = {'token': token, 'user': name}
        return jsonify(response)
    return 'ERROR'


if __name__ == '__main__':
    app.run()
