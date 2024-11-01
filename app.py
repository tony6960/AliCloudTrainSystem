from flask import Flask, request, render_template, make_response, redirect, url_for
import sqlite3
from ats_checker import *
from ats_info import *

app = Flask(__name__)
conn = sqlite3.connect('ATS.db', check_same_thread=False)
cursor = conn.cursor()
user_list = []


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


if __name__ == '__main__':
    app.run()
