from flask import Flask, request, jsonify, redirect
from werkzeug.utils import secure_filename

from data import db_session
from data.photos import Photo
from data.users import User
from data.additional_information import Info

from flask_jwt_extended import JWTManager, jwt_required
from flask_cors import CORS
from config import Config

# from s3 import s3
from settings import settings

from sqlalchemy.exc import IntegrityError, NoResultFound

app = Flask(__name__)
cors = CORS(app)
app.config['SECRET_KEY'] = Config.SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = Config.SQLALCHEMY_DATABASE_URI

jwt = JWTManager(app)


@app.route("/registration", methods=["POST"])
def registration():
    db_sess = db_session.create_session()
    params = request.json
    if not db_sess.query(User).filter_by(login=params['login']).first():
        user = User(
            name=params['name'],
            login=params['login'],
            age=params['age'],
            sex=params['sex']
        )
        user.set_password(params['password'])

        db_sess.add(user)
        db_sess.commit()
    # try:

    # except IntegrityError:
    else:
        return {'access': 'Такой пользователь уже существует'}
    # token = user.get_token()

    return {'access': 'Пользователь создан', 'status_code': 200}
    # return jsonify({'access': 'OK'})


@app.route('/login', methods=['POST'])
def login():
    db_sess = db_session.create_session()
    params = request.json
    try:
        user = db_sess.query(User).filter(params['login'] == User.login).one()
    except NoResultFound:
        return {'access': 'Неверно указан логин', 'exception': 'NoResultFound'}
    if not user.check_password(params['password']):
        return {'access': 'Неверно указан пароль'}
    return {'access': 'Все указано верно', 'status_code': 200}
    # token = user.get_token()
    # return {'access_token': token}


@app.route('/profile', methods=['POST'])
def profile():
    db_sess = db_session.create_session()
    info = db_sess.query(User).filter(request.json['login'] == User.login).one()
    if info:
        res = {
            'name': info.name,
            'age': info.age,
            'sex': info.sex,
            'access': 'Всё прошло удачно'
        }
        return jsonify(res)
    return {'access': 'Пользователь не найден'}


@app.route('/user_info', methods=['PUT'])
def post_user_info():
    db_sess = db_session.create_session()
    params = request.json
    user = db_sess.query(User).filter_by(login=params['login']).first()
    if user:
        db_sess.query(Info).filter(user.login == Info.user_login). \
            update({'about_me': params['about_me'],
                    'interests': params['interests'],
                    'z': params['z'],
                    'height': params['height'],
                    'education': params['education']})
        db_sess.commit()
        return {'access': 'Данные перезаписаны'}
    return {'access': 'Пользователь не найден'}


@app.route('/user_info', methods=['GET', 'POST'])
def update_user_info():
    db_sess = db_session.create_session()
    params = request.json
    user = db_sess.query(User).filter(params['login'] == User.login).first()
    if db_sess.query(Info).filter(params['login'] == Info.user_login).first():
        return {'access': 'Используйте метод PUT, чтобы перезаписать данные'}
    if user:
        if request.method == 'POST':
            dop_info = Info(
                about_me=params['about_me'],
                interests=params['interests'],
                z=params['z'],
                height=params['height'],
                education=params['education']
            )
            user.add_info = dop_info
            db_sess.commit()
            db_sess.add(dop_info)
            return {'access': 'Информация добавлена'}
    return {'access': 'Пользователь не найден'}


@app.route('/user_info/<user_login>', methods=["GET"])
def get_user_info(user_login):
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(user_login == User.login).first()
    if user:
        return jsonify({'about_me': user.add_info.about_me,
                        'interests': user.add_info.interests,
                        'z': user.add_info.z,
                        'height': user.add_info.height,
                        'education': user.add_info.education,
                        'access': 'Всё прошло удачно'})
    return {'access': 'Пользователь не найден'}


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
                return {'access': 'photo uploaded'}
    return {'access': 'nothing'}


def main():
    db_session.global_init('db/data_of_users.db')
    app.run(debug=True)


if __name__ == '__main__':
    main()
