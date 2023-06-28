
from flask import Blueprint, Response, render_template, request, redirect, url_for
from flask_login import current_user, login_required

from test_app.models import db, User

users = Blueprint('users', __name__)


# ユーザ一覧ページ
@users.route("/users",methods=['GET'])
def users_get():
    users = User.query.all()
    return render_template('users/users_get.html', users=users)

# ユーザー追加処理
@users.route("/users",methods=['POST'])
def users_post():
    user = User(name=request.form["user_name"], mail=request.form["mail"])
    #パスワードを安全に保存
    user.set_password(request.form["password"])
    db.session.add(user)
    db.session.commit()
    return redirect(url_for('users.users_get'))

@users.route("/users/<id>",methods=['GET'])
@login_required
def users_id_get(id):
    # ログインユーザのIDを取得し、自分の個別ページのみ開けるようにする
    if str(current_user.id) != str(id):
        return Response(response="他人の個別ページは開けません", status=403)
    user = User.query.get(id)
    return render_template('users/users_id_get.html', user=user)

@users.route("/users/<id>/edit",methods=['POST'])
def users_id_post_edit(id):
    user = User.query.get(id)
    user.name = request.form["user_name"]
    user.age = request.form["user_age"]
    db.session.merge(user)
    db.session.commit()
    return redirect(url_for('users.users_get'))

@users.route("/users/<id>/delete",methods=['POST'])
def users_id_post_delete(id):
    user = User.query.get(id)
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for('users.users_get'))