from flask import Flask, request, render_template, session, redirect, flash,abort
from datetime import timedelta
from models import dbConnect
from user import User
import hashlib
import uuid
import re

# ↓test用。最終発表版では削除
import pymysql
from db import db
# ↑ここまで


app = Flask(__name__)
app.secret_key = uuid.uuid4().hex
app.permanent_session_lifetime = timedelta(days=30)

#チャンネル一覧の表示
@app.route('/')
def index():
    uid = session.get("uid")
    if uid is None:
        return redirect('/login')
    else:
        channels = dbConnect.getChannelAll()
        channels.reverse()
        username = dbConnect.getUsername(uid)["user_name"]
    return render_template('index.html', channels=channels ,username=username, uid=uid)

#ログインページの表示
@app.route('/login')
def login():
    return render_template('/login.html')


# ログイン処理
@app.route('/login', methods=['POST'])
def userLogin():
    name = request.form.get('username')
    password = request.form.get('password')

    if name =='' or password == '':
        flash('空のフォームがあるようです')
    else:
        user = dbConnect.getUserFromName(name)
        if user is None:
            flash('このユーザーは存在しません')
        else:
            hashPassword = hashlib.sha256(password.encode('utf-8')).hexdigest()
            if hashPassword != user["password"]:
                flash('パスワードが間違っています！')
            else:
                session['uid'] = user["uid"]
                return redirect('/')
    return redirect('/login')


# ログアウト
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')


#サインアップページの表示
@app.route('/signup')
def signup():
    return render_template('/signup.html')

#サインアップ処理
@app.route('/signup', methods=['POST'])
def userSignup():
    name = request.form.get('username')
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
            UserId = str(uid)
            session['uid'] = UserId
            return redirect('/')
    return redirect('/signup')

# チャンネル詳細ページの表示
@app.route('/detail/<cid>')
def detail(cid):
    uid = session.get("uid")
    if uid is None:
        return redirect('/login')

    cid = cid
    channel = dbConnect.getChannelById(cid)
    messages = dbConnect.getMessageAll(cid)

    return render_template('detail.html', messages=messages, channel=channel, uid=uid)


#チャンネル追加ページの表示
@app.route('/add-channel')
def addchannel():
    return render_template('/add-channel.html')

# チャンネルの追加
@app.route('/add-channel', methods=['POST'])
def add_channel():
    uid = session.get('uid')
    # return render_template('/add-channel.html', uid=uid)
    
    if uid is None:
        return redirect('login')
    
    channel_name = request.form.get('channelTitle')
    channel = dbConnect.getChannelByName(channel_name)
    if channel == None:
        channel_description = request.form.get('channelDescription')
        dbConnect.addChannel(uid, channel_name, channel_description)
        return redirect('/')
    else:
        error = '既に同じ名前のチャンネルが存在しています'
        return render_template('error/error.html', error_message=error)
    
    
    return render_template('/add-channel.html')



# メッセージの新規投稿
@app.route('/message', methods=['POST'])
def add_message():
    uid = session.get("uid")
    if uid is None:
        return redirect('/login')

    message = request.form.get('url-message')
    cid = request.form.get('cid')

    if message:
        dbConnect.createMessage(uid, cid, message)

    return redirect('/detail/{cid}'.format(cid = cid))


# メッセージの削除
@app.route('/delete_message', methods=['POST'])
def delete_message():
    uid = session.get("uid")
    if uid is None:
        return redirect('/login')

    message_id = request.form.get('message-id')
    cid = request.form.get('cid')

    if message_id:
        dbConnect.deleteMessage(message_id)

    return redirect('/detail/{cid}'.format(cid = cid))



@app.route('/test')
def test():
        test = ""
        cur = None
        conn = db.getConnection()
        cur = conn.cursor()
        sql = "SELECT email FROM users;"
        cur.execute(sql)
        channels = cur.fetchall()
        for i in range(len(channels)):
            test = test + ',' + str(channels[i]['email'])
        
        return render_template('/test.html',test = test)

## おまじない
if __name__ == "__main__":
    app.run(host="0.0.0.0",debug=True)
