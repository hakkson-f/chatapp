from flask import Flask, request, render_template, session, redirect, flash,abort
from datetime import timedelta
from models import dbConnect
from user import User
import hashlib
import uuid
import re


#ログインメール通知設定
from flask_mail import Mail, Message

# ↓test用。最終発表版では削除
import pymysql
from db import db
# ↑ここまで


app = Flask(__name__)
app.secret_key = uuid.uuid4().hex
app.permanent_session_lifetime = timedelta(days=30)


#メール設定
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587                             # TLSは587、SSLなら465
app.config['MAIL_USERNAME'] = 'hackathon0701@gmail.com'
app.config['MAIL_PASSWORD'] = 'cvvrnryfkhutmltq'        # GmailのApp用のmパスワード設定をしておく必要あり
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_DEFAULT_SENDER'] = 'hackathon'    # これがあるとsender設定が不要になる
mail = Mail(app)


#チャンネル一覧の表示
@app.route('/')
def index():
    uid = session.get("uid")
    if uid is None:
        return redirect('/login')
    else:
        channels = dbConnect.getChannelAll(uid)
        if len(channels) != 0:
            channels.reverse()
        username = dbConnect.getUsername(uid)["user_name"]
    return render_template('index-2.html', channels=channels ,username=username, uid=uid)


#チャンネル検索結果の表示
@app.route('/search-channels', methods=['POST'])
def searchChannels():
    uid = session.get("uid")
    if uid is None:
        return redirect('/login')
    else:
        channel_name=request.form.get('search-channels')
        channels = dbConnect.searchChannels(uid,channel_name)
        if len(channels) != 0:
            channels.reverse()
        username = dbConnect.getUsername(uid)["user_name"]
            
    return render_template('search-channel-2.html', channels=channels ,username=username, uid=uid)


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
                #ログインメール通知
                msg = Message('ログイン通知', recipients=[user['email']])
                msg.body = ""+user['user_name']+"さん、TechTalkへのログインを検知しました。\n" 
                mail.send(msg)

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
    return render_template('/signup-2.html')

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
    
    
    # retusrn render_template('/add-channel.html')


#チャンネル情報の更新ページの表示
@app.route('/update-channel')
def updatechannel():
    cid = request.form.get('cid')
    print(cid)
    channel = dbConnect.getChannelById(cid)
    print(channel)
    return render_template('/update-channel.html', channel=channel)
    
#チャンネル削除機能
@app.route('/delete_channel', methods=['POST'])
def deletechannel():
    uid = session.get("uid")
    print(uid)
    if uid is None:
        return redirect('/login')
    else:
        cid = request.form.get('cid')
        channel = dbConnect.getChannelById(cid)
        # print(channel["uid"] == uid)
        if channel["uid"] != uid:
            flash('チャンネルは作成者のみ削除可能です')
            return redirect('/')
        else:
            dbConnect.deletechannel(cid)
            channels = dbConnect.getChannelAll(uid)
            channels=channels[::-1]
            return render_template('index-2.html', channels=channels, uid=uid)


#お気に入りチャンネル一覧の表示
@app.route('/favorites')
def favorites():
    uid = session.get("uid")
    if uid is None:
        return redirect('/login')
    else:
        channels = dbConnect.getFavoriteChannelAll(uid)
        if channels != None:
            channels=channels[::-1]
        username = dbConnect.getUsername(uid)["user_name"]
    return render_template('favorites-2.html', channels=channels ,username=username, uid=uid)


#お気に入りチャンネルの登録
@app.route('/favorites_channel', methods=['POST'])
def addfavoritesChannel():
    uid = session.get("uid")
    if uid is None:
        return redirect('/login')
    else:
        cid = request.form.get('cid')
        channels = dbConnect.addFavoriteChannel(uid,cid)
        
        return redirect('/')


#お気に入りチャンネル解除機能
@app.route('/delete_favoritechannel', methods=['POST'])
def deletefavoriteChannel():
    uid = session.get("uid")
    print(uid)
    if uid is None:
        return redirect('/login')
    else:
        favorite_id = request.form.get('cid')
        
        dbConnect.deletefavoritechannel(favorite_id)
        
        channels = dbConnect.getFavoriteChannelAll(uid)
        if channels != None:
            channels[::-1]
        username = dbConnect.getUsername(uid)["user_name"]
        return render_template('favorites-2.html', channels=channels ,username=username, uid=uid)


#チャンネル一覧からお気に入りチャンネル解除
@app.route('/delete_favoritechannel-index', methods=['POST'])
def deletefavoriteChannel_index():
    uid = session.get("uid")
    print(uid)
    if uid is None:
        return redirect('/login')
    else:
        favorite_id = request.form.get('cid')
        
        dbConnect.deletefavoritechannel(favorite_id)
        
        channels = dbConnect.getFavoriteChannelAll(uid)
        if channels != None:
            channels[::-1]
        username = dbConnect.getUsername(uid)["user_name"]
        return redirect('/')




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



# パスワードお忘れですか？ページの表示
@app.route('/forgot-password')
def forgotPassword():
    return render_template('forgot-password.html')


# パスワードお忘れですか？からメールを送る
@app.route('/forgot-password', methods=['POST'])
def passwordChangeUrlMail():
    sendemail = request.form.get('email')
    user=dbConnect.getUser(sendemail)
    if user is None :
        flash('このメールアドレスのユーザーは登録されていません') 

    else:
    #パスワード再設定用メール通知
        msg = Message('パスワード再設定用URL', recipients=[sendemail])
        msg.body = ""+user['user_name']+"さん、TechTalkにアクセスしてパスワード再設定をしてください。\n AWS用： https://tech-talk-chat.net:5000/password-change/"+ user['password'] +" \n ローカル用： http://127.0.0.1:5000/password-change/"+ user['password'] +" にアクセスしてください。\n" 
        mail.send(msg)

        flash('メールを送りました') 

    return render_template('forgot-password.html')


# パスワード変更ページの表示
@app.route('/password-change/<passhash>')
def passwordChange(passhash):
    passhash = passhash
    user = dbConnect.getUserFromPass(passhash)
    if user is None :
        return redirect('/login')

    return render_template('password-change.html', user=user)



# パスワード変更処理
@app.route('/password-change/<passhash>', methods=['POST'])
def updataPassword(passhash):
    passhash = passhash
    user = dbConnect.getUserFromPass(passhash)
    password1 = request.form.get('password1')
    password2 = request.form.get('password2')

    if password1 == '' or password2 == '':
        flash('空のフォームがあります') 
    elif password1 != password2:
        flash('パスワードが一致しません')
    else:
        password = hashlib.sha256(password1.encode('utf-8')).hexdigest()
        dbConnect.updateUser(user['uid'], user['user_name'], user['email'], password)
        UserId = str(user['uid'])
        session['uid'] = UserId
        #パスワード再設定通知
        msg = Message('パスワード再設定通知', recipients=[user['email']])
        msg.body = ""+user['user_name']+"さん、TechTalkのパスワード再設定を検知しました。\n" 
        mail.send(msg)

        return redirect('/')
    
    return render_template('password-change.html', user=user)


#プロフィールページの表示
@app.route('/profile')
def profile():
    uid = session.get("uid")
    if uid is None:
        return redirect('/login')
    else:
        user = dbConnect.getUsername(uid)
    
    return render_template('/profile.html', user=user)


#その他のプロフィールページの表示
@app.route('/profile-other')
def profileother():
    uid = session.get("uid")
    if uid is None:
        return redirect('/login')
    else:
        user = dbConnect.getUsernameOther(uid)
    
    return render_template('/profile-other.html', user=user)


@app.route('/test')
def test():
        test = ""
        cur = None
        conn = db.getConnection()
        cur = conn.cursor()
        sql = "SELECT * FROM users;"
        cur.execute(sql)
        channels = cur.fetchall()
        for i in range(len(channels)):
            test = test + ',' + str(channels[i]['email'])
        
        return render_template('/test.html',test = test)

@app.route('/test2')
def test2():
        
        cur = None
        conn = db.getConnection()
        cur = conn.cursor()
        sql = "SELECT * FROM users;"
        cur.execute(sql)
        channels = cur.fetchall()
        
        return render_template('/test.html',test = channels)


@app.errorhandler(404)
def show_error404(error):
    return render_template('404.html'),404


@app.errorhandler(500)
def show_error500(error):
    return render_template('500.html'),500

## おまじない
if __name__ == "__main__":
    app.run(host="0.0.0.0",debug=True)