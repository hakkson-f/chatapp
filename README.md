# chatapp

**起動方法**
```
docker compose up
```

### ディレクトリ構成
```
.
├── chatapp-techtalk              # pythonファイル、html、css、js,icon画像ディレクトリ
│   ├── __init__.py
│   ├── app.py
│   ├── models.py
│   ├── db.py           # MySQLへの接続設定ファイル
│   ├── user.py           # MySQLへuser情報を入力する際のテンプレ
│   ├── static          # 静的ファイル用ディレクトリ
│   └── templates       # Template(HTML)用ディレクトリ
│  
├── Docker
│   ├── Flask
│   │   └── Dockerfile # Flask(Python)用Dockerファイル
│   └── MySQL
│       ├── Dockerfile  # MySQL用Dockerファイル
│       ├── init.sql    # MySQL初期設定ファイル
│       └── my.cnf
├── docker-compose.yml   # Docker-composeファイル
└── requirements.txt     # 使用モジュール記述ファイル
```