import pymysql
from db import db

#ユーザー登録処理
class dbConnect:
    def createUser(user):
        try:
            conn = db.getConnection()
            cur = conn.cursor()
            sql = "INSERT INTO users (uid, user_name, email, password) VALUES (%s, %s, %s, %s);"
            cur.execute(sql, (user.uid, user.name, user.email, user.password))
            conn.commit()
        except Exception as e:
            print(e + 'が発生しています')
            abort(500)
        finally:
            cur.close()

#ユーザー情報の取得
    def getUser(email):
        try:
            conn = db.getConnection()
            cur = conn.cursor()
            sql = "SELECT * FROM users WHERE email=%s;"
            cur.execute(sql, (email))
            user = cur.fetchone()
            return user 
        except Exception as e:
            print(e + 'が発生しています')
            abort(500)
        finally:
            cur.close()


    #ユーザー情報の取得（名前から）
    def getUserFromName(name):
        try:
            conn = db.getConnection()
            cur = conn.cursor()
            sql = "SELECT * FROM users WHERE user_name=%s;"
            cur.execute(sql, (name))
            user = cur.fetchone()
            return user 
        except Exception as e:
            print(e + 'が発生しています')
            abort(500)
        finally:
            cur.close()

    
    #ユーザー情報の取得（passwordハッシュ値から）
    def getUserFromPass(passhash):
        try:
            conn = db.getConnection()
            cur = conn.cursor()
            sql = "SELECT * FROM users WHERE password=%s;"
            cur.execute(sql, (passhash))
            user = cur.fetchone()
            return user 
        except Exception as e:
            print(e + 'が発生しています')
            abort(500)
        finally:
            cur.close()


    def updateUser(uid, newUserName, newUserEmail, password):
        try:
            conn = db.getConnection()
            cur = conn.cursor()
            sql = "UPDATE users SET user_name=%s, email=%s, password=%s WHERE uid=%s;"
            cur.execute(sql, (newUserName, newUserEmail, password, uid))
            conn.commit()
        except Exception as e:
            print(e + 'が発生しました')
            abort(500)
        finally:
            cur.close()




    #ユーザー名の取得
    def getUsername(uid):
        try:
            conn = db.getConnection()
            cur = conn.cursor()
            sql = "SELECT user_name,email FROM users WHERE uid=%s;"
            cur.execute(sql, (uid))
            user = cur.fetchone()
            return user 
        except Exception as e:
            print(e + 'が発生しています')
            abort(500)
        finally:
            cur.close()

    
    #その他のユーザー名の取得
    def getUsernameOther(uid):
        try:
            conn = db.getConnection()
            cur = conn.cursor()
            sql = "SELECT user_name,email FROM users WHERE uid !=%s;"
            cur.execute(sql,(uid))
            user = cur.fetchall()
            return user 
        except Exception as e:
            print(e + 'が発生しています')
            abort(500)
        finally:
            cur.close()


      # チャンネル一覧を取得
    def getChannelAll():
      cur = None
      try:
        conn = db.getConnection()
        cur = conn.cursor()
        sql = "SELECT * FROM channels;"
        cur.execute(sql)
        channels = cur.fetchall()
        return channels
      except Exception as e :
        print(str(e) + 'が発生しています')
        return None
      finally:
        if cur is not None:
          cur.close()


    
      # チャンネル検索結果を取得
    def searchChannels(channel_name):
      cur = None
      try:
        conn = db.getConnection()
        cur = conn.cursor()
        sql = "SELECT * FROM channels WHERE name like '%"+channel_name+"%';"
        cur.execute(sql)
        channels = cur.fetchall()
        return channels
      except Exception as e :
        print(str(e) + 'が発生しています')
        return None
      finally:
        if cur is not None:
          cur.close()


    # 同じchannel名があるか確認
    def getChannelByName(channel_name):
        try:
            conn = db.getConnection()
            cur = conn.cursor()
            sql = "SELECT * FROM channels WHERE name=%s;"
            cur.execute(sql, (channel_name))
            channel = cur.fetchone()
            return channel
        except Exception as e:
            print(str(e) + 'が発生しています')
            return None
        finally:
            cur.close()

    
    #チャンネル追加
    def addChannel(uid, newChannelName, newChannelDescription):
        try:
            conn = db.getConnection()
            cur = conn.cursor()
            sql = "INSERT INTO channels (uid, name, abstract) VALUES (%s, %s, %s);"
            cur.execute(sql, (uid, newChannelName, newChannelDescription))
            conn.commit()
        except Exception as e:
            print(str(e) + 'が発生しています')
            return None
        finally: 
            cur.close()

    #チャンネル削除
    def deletechannel(cid):
        try:
            conn = db.getConnection()
            cur = conn.cursor()
            sql = "DELETE FROM channels WHERE id=%s;"
            cur.execute(sql, (cid))
            conn.commit()
        except Exception as e:
            print(e + 'が発生しています')
            return None
        finally:
             cur.close()

     # チャンネル詳細ページに移行するためのチャンネルデータ取得
    def getChannelById(cid):
        try:
            conn = db.getConnection()
            cur = conn.cursor()
            sql = "SELECT * FROM channels WHERE id=%s;"
            cur.execute(sql, (cid))
            channel = cur.fetchone()
            return channel
        except Exception as e:
            print(e + 'が発生しています')
            abort(500)
        finally:
            cur.close()


     # チャンネルに紐づくメッセージ一覧を取得
    def getMessageAll(cid):
        try:
            conn = db.getConnection()
            cur = conn.cursor()
            sql = "SELECT id,users.uid, user_name, message,created_at FROM messages INNER JOIN users ON messages.uid = users.uid WHERE cid = %s;"
            cur.execute(sql, (cid))
            messages = cur.fetchall()
            return messages
        except Exception as e:
            print(e + 'が発生しています')
            abort(500)
        finally:
            cur.close()

     # メッセージの新規投稿をデータベースへ反映
    def createMessage(uid, cid, message):
        try:
            conn = db.getConnection()
            cur = conn.cursor()
            sql = "INSERT INTO messages(uid, cid, message) VALUES(%s, %s, %s)"
            cur.execute(sql, (uid, cid, message))
            conn.commit()
        except Exception as e:
            print(e + 'が発生しています')
            abort(500)
        finally:
            cur.close()

     # メッセージの削除をデータベースへ反映
    def deleteMessage(message_id):
        try:
            conn = db.getConnection()
            cur = conn.cursor()
            sql = "DELETE FROM messages WHERE id=%s;"
            cur.execute(sql, (message_id))
            conn.commit()
        except Exception as e:
            print(e + 'が発生しています')
            abort(500)
        finally:
            cur.close()