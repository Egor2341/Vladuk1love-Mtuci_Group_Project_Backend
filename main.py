import os

from flask import Flask, request, jsonify, redirect
from werkzeug.utils import secure_filename

from data import db_session
from data.photos import Photo
from data.users import User
from flask_jwt_extended import JWTManager, jwt_required
from flask_cors import CORS

from s3 import s3
from settings import settings

app = Flask(__name__)
cors = CORS(app)
app.config['SECRET_KEY'] = 'my_own_secret_key'
jwt = JWTManager(app)

@app.route("/registration", methods=["POST"])
def registration():
    db_sess = db_session.create_session()
    params = request.json
    user = User(
        name=params['name'],
        login=params['login'],
        age=params['age'],
        sex=params['sex']
    )
    user.set_password(params['password'])
    db_sess.add(user)
    try:
        db_sess.commit()
    except:
        return 'Пользователь уже существует'
    # token = user.get_token()
    # return {'access_token': token}
    return 'OK'


@app.route('/login', methods=['POST'])
def login():
    db_sess = db_session.create_session()
    params = request.json
    try:
        user = db_sess.query(User).filter(params['login'] == User.login).one()
    except:
        return 'Неверно указан логин'
    # try:
    #     user.check_password(params['password'])
    # except:
    #     return 'Неверно указан пароль'
    if not user.check_password(params['password']):
        return 'Неверно указан пароль'
    return 'Все указано верно'
    # token = user.get_token()
    # return {'access_token': token}


@app.route('/profile', methods=['POST'])
def profile():
    db_sess = db_session.create_session()
    login = request.json['login']
    info = db_sess.query(User).filter(login == User.login).one()
    res = {
        'name': info.name,
        'age': info.age,
        'sex': info.sex
    }
    return jsonify(res)


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in settings.ALLOWED_EXTENSIONS


@app.route('/photos/<user_login>', methods=['GET', 'POST'])
def photos(user_login):
    db_sess = db_session.create_session()
    if db_sess.query(User).filter(user_login == User.login).all() != []:
        if request.method == 'POST':
            if 'file' not in request.files:
                return 'not file'
            file = request.files['file']
            if file.filename == '':
                return 'not filename'
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                s3.upload_file(file, f'{user_login}_{filename}')
                photo = Photo(
                    user_login=user_login,
                    img=settings.AWS_BUCKET,
                    name=filename
                )
                db_sess.add(photo)
                db_sess.commit()
                return 'photo uploaded'
    return 'nothing'


def main():
    db_session.global_init('db/data_of_users.db')
    app.run(debug=True)


if __name__ == '__main__':
    main()
