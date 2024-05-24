# импорт flask
from flask import Flask, request, jsonify
# импорт моделей
from data import db_session
from data.photos import Photo
from data.users import User
from data.additional_information import Info
from data.preferences import Preference
from data.likes import MyLikes, WhoLikedMe
# from flask_jwt_extended import JWTManager, jwt_required
from flask_cors import CORS
from config import Config
from flask_socketio import SocketIO, emit

from s3 import s3
from settings import settings

from waitress import serve

from sqlalchemy.sql import func

app = Flask(__name__)
cors = CORS(app)
app.config['SECRET_KEY'] = Config.SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = Config.SQLALCHEMY_DATABASE_URI
app.config['CORS_HEADERS'] = 'Content-Type'



socketio = SocketIO(app, cors_allowed_origins="*")


@socketio.on('message')
def handle_message(user):
    db_sess = db_session.create_session()
    logins = list(db_sess.query(WhoLikedMe).filter(WhoLikedMe.user_who_was_liked == user))
    names = list(db_sess.query(User).filter(User.login == user))
    if len(logins) != 0:
        socketio.emit('message',
                  {'logins': list(map(lambda x: x.user_login, logins)),
                   'names': list(map(lambda x: x.name, names))})

@socketio.on('text')
def handle_text(text):
    print(text)
    socketio.emit('text', 'fdsafasd')

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
            dating_purpose='Дружба'
        )
        user.add_info = dop_info
        db_sess.commit()
        db_sess.add(dop_info)

        pref = Preference(
        )
        user.preferences = pref
        db_sess.commit()
        db_sess.add(pref)

        login = params['login']

        photo = Photo(img_s3_location=f'{str(login)}_avatar')
        photo.user_img = user
        db_sess.add(photo)
        db_sess.commit()

        photo = 'default_photo.png'
        with open(photo, 'rb') as data:
            s3.upload_file(data, f'{login}_avatar')

        return jsonify({'access': 'Пользователь создан', 'status_code': 201})
    else:
        return jsonify({'access': 'Такой пользователь уже существует',
                        'status_code': 403})


@app.route('/login', methods=['POST'])
def login():
    db_sess = db_session.create_session()
    password = request.json.get('password')
    login = request.json.get('login')
    user = db_sess.query(User).filter_by(login=login).first()
    if not user:
        return jsonify({'access': 'Неверно указан логин', 'status_code': 400})
    if not user.check_password(password):
        return jsonify({'access': 'Неверно указан пароль', 'status_code': 400})
    return jsonify({'access': 'Все указано верно', 'status_code': 200})


@app.route('/found_users_on_the_main_page/<user_login>', methods=['POST'])
def find_users(user_login):
    params = request.json
    db_sess = db_session.create_session()
    logined_user = db_sess.query(User).filter_by(login=user_login).first()
    response = {}
    if logined_user:
        users_8 = db_sess.query(User) \
            .filter(User.login != logined_user.login,
                    User.age.between(*params['age']),
                    User.sex.in_(params['sex']),
                    User.add_info.has(Info.dating_purpose.in_(params['dating_purpose']))
                    ) \
            .order_by(func.random()).limit(8).all()
        for i in range(len(users_8)):
            response[f'user{i}'] = {'id': i + 1,
                                    'name': users_8[i].name,
                                    'login': users_8[i].login,
                                    'age': users_8[i].age,
                                    'sex': users_8[i].sex,
                                    'dating_purpose': users_8[i].add_info.dating_purpose,
                                    'photo': [i.s3_url for i in users_8[i].photos]
                                    }

        return jsonify(response)
    return {'access': 'Пользователь не найден', 'status_code': 404}


@app.route('/card/<user_login>', methods=['GET'])
def get_card(user_login):
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter_by(login=user_login).first()
    if user:
        return jsonify(
            {
                'name': user.name,
                'group': user.add_info.group,
                'age': user.age,
                'sex': user.sex,
                'dating_purpose': user.add_info.dating_purpose,
                'about_me': user.add_info.about_me,
                'photo': [i.s3_url for i in user.photos]
            }
        )
    return {'access': 'Пользователь не найден', 'status_code': 404}


@app.route('/likes/<user_login>', methods=['POST'])
def i_liked(user_login):
    who_i_liked = request.json.get('who_i_liked')
    if who_i_liked:
        db_sess = db_session.create_session()
        my_like = db_sess.query(MyLikes).filter_by(user_login=user_login, who_i_liked=who_i_liked).first()
        liked_by = db_sess.query(WhoLikedMe).filter_by(user_login=who_i_liked,
                                                       user_who_was_liked=user_login).first()

        if my_like and liked_by:
            db_sess.delete(my_like)
            db_sess.delete(liked_by)
            db_sess.commit()
            return {'access': 'Лайк успешно удалён', 'status_code': 204}

        i_like = MyLikes(
            who_i_liked=who_i_liked
        )
        i_like.user_login = user_login

        liked_me = WhoLikedMe(
            user_login=who_i_liked
        )
        liked_me.user_who_was_liked = user_login

        db_sess.add_all([i_like, liked_me])
        db_sess.commit()
        return jsonify(
            {'access': f'Вы успешно лайкнули пользователя: {who_i_liked}', 'status_code': 204}
        )

    return jsonify({'access': 'Пользователь не найден', 'status_code': 404})


@app.route('/who_liked_me/<user_login>', methods=['GET'])
def who_liked_me(user_login):
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter_by(login=user_login).first()
    if user:
        return jsonify(
            {'users_who_liked_me': [i.user_login for i in user.who_liked_me]}
        )
    return jsonify({'access': 'Пользователь не найден', 'status_code': 404})


@app.route('/who_i_liked/<user_login>', methods=['GET'])
def who_i_liked(user_login):
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter_by(login=user_login).first()
    if user:
        return jsonify(
            {'users_who_i_liked': [i.who_i_liked for i in user.my_likes]}
        )
    return jsonify({'access': 'Пользователь не найден', 'status_code': 404})


@app.route('/get_like_from_card/<user_login>', methods=['POST'])
def get_like_from_card(user_login):
    card_user = request.json.get('card_login')
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter_by(login=user_login).first()
    if user:
        like_exists = db_sess.query(MyLikes).filter_by(user_login=user_login,
                                                       who_i_liked=card_user
                                                       ).scalar()
        return jsonify(
            {'access': bool(like_exists)}
        )
    return jsonify({'access': 'Пользователь не найден', 'status_code': 404})


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
    return jsonify({'access': 'Пользователь не найден', 'status_code': 404})


# для доп инфы
@app.route('/user_info/<user_login>', methods=["GET"])
def get_user_info(user_login):
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter_by(login=user_login).first()
    if user:
        return jsonify({
            'name': user.name,
            'age': user.age,
            'sex': user.sex,
            'about_me': user.add_info.about_me,
            'interests': user.add_info.interests,
            'group': user.add_info.group,
            'dating_purpose': user.add_info.dating_purpose,
            'education': user.add_info.education
        })
    return jsonify({'access': 'Пользователь не найден', 'status_code': 404})


@app.route('/user_info/<user_login>', methods=['PUT'])
def post_user_info(user_login):
    db_sess = db_session.create_session()
    params = request.json
    user = db_sess.query(User).filter_by(login=user_login).first()
    if user:
        db_sess.query(Info).filter_by(user_login=user.login). \
            update({'about_me': params['about_me'],
                    'interests': params['interests'],
                    'group': params['group'],
                    'dating_purpose': params['dating_purpose'],
                    'education': params['education']})
        db_sess.commit()
        return jsonify({'access': 'Данные перезаписаны', 'status_code': 200})
    return jsonify({'access': 'Пользователь не найден', 'status_code': 404})


# делаю для предпочтений
@app.route('/user_preferences/<user_login>', methods=["GET"])
def get_user_preferences(user_login):
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter_by(login=user_login).first()
    if user:
        return jsonify({
            'age_pref': user.preferences.age_pref,
            'height_pref': user.preferences.height_pref,
            'weight_pref': user.preferences.weight_pref,
            'type': user.preferences.type,
            'habits': user.preferences.habits,
            'religion': user.preferences.religion
        })
    return jsonify({'access': 'Пользователь не найден', 'status_code': 404})


@app.route('/user_preferences/<user_login>', methods=['PUT'])
def post_user_preferences(user_login):
    db_sess = db_session.create_session()
    params = request.json
    user = db_sess.query(User).filter_by(login=user_login).first()
    if user:
        db_sess.query(Preference).filter_by(user_login=user_login). \
            update({'age_pref': params['age_pref'],
                    'height_pref': params['height_pref'],
                    'weight_pref': params['weight_pref'],
                    'type': params['type'],
                    'habits': params['habits'],
                    'religion': params['religion']})
        db_sess.commit()
        return jsonify({'access': 'Данные перезаписаны', 'status_code': 200})
    return jsonify({'access': 'Пользователь не найден', 'status_code': 404})


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in settings.ALLOWED_EXTENSIONS


@app.route('/up_photos/<user_login>/<avatar>', methods=['GET', 'POST'])
def up_photos(user_login, avatar):
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(user_login == User.login).first()
    if user:
        if request.method == 'POST':
            if 'file' not in request.files:
                return 'not file'
            file = request.files['file']
            if file.filename == '':
                return 'not filename'
            if file and allowed_file(file.filename):
                photos = [i.img_s3_location for i in user.photos]
                name = 'avatar' if avatar == 'avatar' else 'img' + str(len(photos))
                s3.upload_file(file, f'{user_login}_{name}')
                if photos[0] == '':
                    db_sess.query(Photo).filter(user.login == Photo.user_login).update(
                        {'img_s3_location': f'{user_login}_{name}'})
                    db_sess.commit()
                elif not (f'{user_login}_{name}' in photos and name == 'avatar'):
                    photo = Photo(img_s3_location=f'{user_login}_{name}')
                    photo.user_img = user
                    db_sess.add(photo)
                    db_sess.commit()
                return jsonify({'access': 'photo uploaded'})
    return jsonify({'access': 'nothing'})


@app.route('/down_photos/<user_login>/<avatar>', methods=['GET', 'POST'])
def down_photos(user_login, avatar):
    db_sess = db_session.create_session()
    if db_sess.query(User).filter(user_login == User.login).first():
        if request.method == 'POST':
            if avatar == 'avatar':
                photo = db_sess.query(Photo).filter(f'{user_login}_avatar' == Photo.img_s3_location).first()
                return photo.s3_url
            photo = list(db_sess.query(Photo).filter(user_login == Photo.user_login))
            return list(map(lambda x: x.s3_url, photo))
    return jsonify({'access': 'Login not found'})


def main():
    db_session.global_init('db/data_of_users.db')
    serve(app, host='127.0.0.1', port='5000')


if __name__ == '__main__':
    main()
