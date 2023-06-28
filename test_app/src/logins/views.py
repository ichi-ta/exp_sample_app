
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, current_user, login_user, login_required, logout_user

from test_app import app
from test_app.models import User

login = LoginManager(app)
logins = Blueprint("logins", __name__)

@login.user_loader
def load_user(id):
    # ログイン機能からidを受け取った際、DBからそのユーザ情報を検索し、返す
    return User.query.get(int(id))


# ページ定義に`@login_required`記述するとログイン必須になる（順番に注意@app, @login, def）
@logins.route("/",methods=['GET'])
@login_required
def index_get():
    return render_template('index.html')

# ログインページの実装
@logins.route('/login', methods=['GET'])
def login_get():
  # 現在のユーザーがログイン済みの場合
  if current_user.is_authenticated:
    # トップページに移動
    return redirect(url_for('logins.index_get'))
  
  # loginページのテンプレートを返す
  return render_template('logins/login.html')


# メールアドレスとパスワードを受け取り処理を行う
@logins.route('/login', methods=['POST'])
def login_post():
    # メールアドレスをもとにデータベースへ問い合わせる
    # 結果がゼロの時はNoneを返す
    user = User.query.filter_by(mail=request.form["mail"]).one_or_none()
    
    # ユーザが存在しない or パスワードが間違っている時
    if user is None or not user.check_password(request.form["password"]):
        # メッセージの表示
        flash('メールアドレスかパスワードが間違っています')
        # loginページへリダイレクト
        return redirect(url_for('logins.login_get'))

    # ログインを承認
    login_user(user)
    # トップページへリダイレクト
    return redirect(url_for('logins.index_get'))


@logins.route('/logout')
def logout():
  # logout_user関数を呼び出し
  logout_user()
  # トップページにリダイレクト
  return render_template('logins/logout.html')

