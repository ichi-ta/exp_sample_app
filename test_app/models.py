from test_app import app
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


DB_USER = "docker"
DB_PASS = "docker"
DB_HOST = "db"
DB_NAME = "flask_app"

app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+mysqldb://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}?charset=utf8"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.secret_key = "secret"

db = SQLAlchemy(app)
migrate = Migrate(app, db)

class User(UserMixin, db.Model):
    # テーブル名を指定
    __tablename__ = 'Users'
    # 数値型のidカラム
    id = db.Column(db.Integer, primary_key=True)
    # 文字列型のnameカラム
    name = db.Column(db.String(128))

     # 認証を行うためメールアドレスとパスワードカラムを追加
    mail = db.Column(db.String(128), unique=True)
    password = db.Column(db.String(128))
    # パスワードをハッシュ化
    def set_password(self, password):
        self.password = generate_password_hash(password)

    # 入力されたパスワードが登録されているパスワードハッシュと一致するかを確認
    def check_password(self, password):
            return check_password_hash(self.password, password)