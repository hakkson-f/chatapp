from flask import Flask, request, render_template, session, redirect, flash
from models import dbConnect
from user import User
import hashlib
import uuid
import re

app = Flask(__name__)

#チャンネル一覧の表示
@app.route('/')
def index():
    uid = session.get("uid")
    if uid is None:
        return redirect('/login')
    else:
        channels = dbConnect.getChannelAll()
        channels.reverse()
    return render_template('index.html', channels=channels)

#ログインページの表示
@app.route('/login')
def login():
    return render_template('/login.html')

#サインアップページの表示
@app.route('/signup')
def signup():
    return render_template('/signup.html')

#サインアップ処理
@app.route('/signup', methods=['POST'])
def userSignup():
    name = request.form.get('name')
    email = request.form.get('email')
    password1 = request.form.get('password1')
    password2 = request.form.get('password2')

    pattern = "^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"

    if name == '' or email == '' or password1 == '' or password2 == '':
        flash('空のフォームがあります') 
    elif password1 != password2:
        flash('パスワードが一致しません')
    elif re.match(pattern, email) is None:
        flash('正しいメールアドレスの形式ではありません')
    else:
        uid = uuid.uuid4()
        password = hashlib.sha256(password1.encode('utf-8')).hexdigest()
        user = User(uid, name, email, password)
        DBuser = dbConnect.getUser(email)

        if DBuser != None:
            flash('既に登録されています')
        else:
            dbConnect.createUser(user)
            UserTd = str(uid)
            session['uid'] = UserId
            return redirect('/')
    return redirect('/signup')

#チャンネル詳細ページの表示
@app.route('/detail')
def detail():
    return render_template('/detail.html')

@app.route('/test')
def test():
    test = "hoge"
    return render_template('/test.html',test = test)

## おまじない
if __name__ == "__main__":
    app.run(debug=True)
