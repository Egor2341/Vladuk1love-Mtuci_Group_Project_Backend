from flask import Flask, request, jsonify, redirect
from werkzeug.utils import secure_filename

from data import db_session
from data.photos import Photo
from data.users import User
from data.additional_information import Info
from data.preferences import Preference

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

        dop_info = Info(
        )
        user.add_info = dop_info
        db_sess.commit()
        db_sess.add(dop_info)

        pref = Preference(
        )
        user.preferences = pref
        db_sess.commit()
        db_sess.add(pref)

    else:
        return {'access': 'Такой пользователь уже существует'}
    # token = user.get_token()

    return {'access': 'Пользователь создан', 'status_code': 200}
    # return jsonify({'access': 'OK'})


@app.route('/login', methods=['POST'])
def login():
    db_sess = db_session.create_session()
    params = request.json
    user = db_sess.query(User).filter_by(login=params['login']).first()
    if not user:
        return {'access': 'Неверно указан логин', 'status_code': 404}
    if not user.check_password(params['password']):
        return {'access': 'Неверно указан пароль', 'status_code': 406}
    return {'access': 'Все указано верно', 'status_code': 200}
    # token = user.get_token()
    # return {'access_token': token}


@app.route('/profile/<user_login>', methods=['GET'])
def profile(user_login):
    db_sess = db_session.create_session()
    info = db_sess.query(User).filter_by(login=user_login).first()
    if info:
        res = {
            'name': info.name,
            'age': info.age,
            'sex': info.sex,
        }
        return jsonify(res)
    return {'access': 'Пользователь не найден', 'status_code': 404}


# для доп инфы
@app.route('/user_info/<user_login>', methods=["GET"])
def get_user_info(user_login):
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter_by(login=user_login).first()
    if user:
        return jsonify({
            'name': ['Имя', user.name],
            'age': ['Возраст', user.age],
            'sex': ['Пол', user.sex],
            'about_me': ['О себе', user.add_info.about_me],
            'interests': ['Интересы', user.add_info.interests],
            'group': ['Группа в МТУСИ', user.add_info.group],
            'dating_purpose': ['Цель знакомства', user.add_info.dating_purpose],
            'education': ['Карьера и Образование', user.add_info.education]
        })
    return {'access': 'Пользователь не найден', 'status_code': 404}


@app.route('/user_info/<user_login>', methods=['PUT'])
def post_user_info(user_login):
    db_sess = db_session.create_session()
    params = request.json
    user = db_sess.query(User).filter_by(login=user_login).first()
    if user:
        db_sess.query(Info).filter_by(user_login=user.login). \
            update({'about_me': params['about_me'][1],
                    'interests': params['interests'][1],
                    'group': params['group'][1],
                    'dating_purpose': params['dating_purpose'][1],
                    'education': params['education'][1]})
        db_sess.commit()
        return {'access': 'Данные перезаписаны', 'status_code': 200}
    return {'access': 'Пользователь не найден', 'status_code': 404}


# делаю для предпочтений
@app.route('/user_preferences/<user_login>', methods=["GET"])
def get_user_preferences(user_login):
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter_by(login=user_login).first()
    if user:
        return jsonify({
            'age_pref': ['Возраст', user.preferences.age_pref],
            'height_pref': ['Рост', user.preferences.height_pref],
            'weight_pref': ['Вес', user.preferences.weight_pref],
            'type': ['Тип внешности', user.preferences.type],
            'habits': ['Вредные привычки', user.preferences.habbits],
            'religion': ['Религия', user.preferences.religion]
        })
    return {'access': 'Пользователь не найден', 'status_code': 404}


@app.route('/user_preferences/<user_login>', methods=['PUT'])
def post_user_preferences(user_login):
    db_sess = db_session.create_session()
    params = request.json
    user = db_sess.query(User).filter_by(login=user_login).first()
    if user:
        db_sess.query(Preference).filter_by(user_login=user_login). \
            update({'age_pref': params['age_pref'][1],
                    'height_pref': params['height_pref'][1],
                    'weight_pref': params['weight_pref'][1],
                    'type': params['type'][1],
                    'habits': params['habits'][1],
                    'religion': params['religion'][1]})
        db_sess.commit()
        return {'access': 'Данные перезаписаны', 'status_code': 200}
    return {'access': 'Пользователь не найден', 'status_code': 404}


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

# groups = [
#     {'value': 'БЭИ-2301', 'label': 'БЭИ-2301'},
#     {'value': 'БЭИ-2302', 'label': 'БЭИ-2302'},
#     {'value': 'БЭИ-2303', 'label': 'БЭИ-2303'},
#
#     {'value': 'БВТ-2301', 'label': 'БВТ-2301'},
#     {'value': 'БВТ-2302', 'label': 'БВТ-2302'},
#     {'value': 'БВТ-2303', 'label': 'БВТ-2303'},
#     {'value': 'БВТ-2304', 'label': 'БВТ-2304'},
#     {'value': 'БВТ-2305', 'label': 'БВТ-2305'},
#     {'value': 'БВТ-2306', 'label': 'БВТ-2306'},
#     {'value': 'БВТ-2307', 'label': 'БВТ-2307'},
#     {'value': 'БВТ-2308', 'label': 'БВТ-2308'},
#
#     {'value': 'БПИ-2301', 'label': 'БПИ-2301'},
#     {'value': 'БПИ-2302', 'label': 'БПИ-2302'},
#     {'value': 'БПИ-2303', 'label': 'БПИ-2303'},
#     {'value': 'БПИ-2304', 'label': 'БПИ-2304'},
#     {'value': 'БПИ-2305', 'label': 'БПИ-2305'},
#     {'value': 'БПИ-2306', 'label': 'БПИ-2306'},
#
#     {'value': 'БСТ-2301', 'label': 'БСТ-2301'},
#     {'value': 'БСТ-2302', 'label': 'БСТ-2302'},
#     {'value': 'БСТ-2303', 'label': 'БСТ-2303'},
#     {'value': 'БСТ-2304', 'label': 'БСТ-2304'},
#
#     {'value': 'БФИ-2301', 'label': 'БФИ-2301'},
#     {'value': 'БФИ-2302', 'label': 'БФИ-2302'}
#
# ]
