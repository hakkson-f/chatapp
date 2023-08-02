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


#ユーザー名の取得
    def getUsername(uid):
        try:
            conn = db.getConnection()
            cur = conn.cursor()
            sql = "SELECT user_name FROM users WHERE uid=%s;"
            cur.execute(sql, (uid))
            user = cur.fetchone()
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