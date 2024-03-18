from flask import Flask, render_template, request, make_response, session, jsonify
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.utils import redirect
from data import db_session
from data.users import User
from forms.user import RegisterForm, LoginForm
from flask_jwt_extended import JWTManager, jwt_required
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app)
# cors = CORS(resources={
#     r'/*': {'origins': 'http://localhost'}
# })
app.config['SECRET_KEY'] = 'my_own_secret_key'
# login_manager = LoginManager()
# login_manager.init_app(app)
jwt = JWTManager(app)


# db_sess = None
# @login_manager.user_loader
# def load_user(user_id):
#     db_sess = db_session.create_session()
#     return db_sess.query(User).get(user_id)


# @app.route("/session_test")
# def session_test():
#     visits_count = session.get('visits_count', 0)
#     session['visits_count'] = visits_count + 1
#     return make_response(
#         f"Вы пришли на эту страницу {visits_count + 1} раз")


# @app.route('/logout')
# @login_required
# def logout():
#     logout_user()
#     return redirect("/")


# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     form = LoginForm()
#     if form.validate_on_submit():
#         db_sess = db_session.create_session()
#         user = db_sess.query(User).filter(User.login == form.login.data).first()
#         if user and user.check_password(form.password.data):
#             login_user(user, remember=form.remember_me.data)
#             return redirect("/")
#         return render_template('login.html',
#                                message="Неправильный логин или пароль",
#                                form=form)
#     return render_template('login.html', title='Авторизация', form=form)


# @app.route("/")
# def index():
#     return render_template("index.html")


# @app.route('/register', methods=['GET', 'POST'])
# def reqister():
#     form = RegisterForm()
#     if form.validate_on_submit():
#         if form.password.data != form.password_again.data:
#             return render_template('register.html', title='Регистрация',
#                                    form=form,
#                                    message="Пароли не совпадают")
#         db_sess = db_session.create_session()
#         if db_sess.query(User).filter(User.login == form.login.data).first():
#             return render_template('register.html', title='Регистрация',
#                                    form=form,
#                                    message="Такой пользователь уже есть")
#         user = User(
#             name=form.name.data,
#             login=form.login.data,
#         )
#         user.set_password(form.password.data)
#         db_sess.add(user)
#         db_sess.commit()
#         return redirect('/login')
#     return render_template('register.html', title='Регистрация', form=form)


@app.route("/registration", methods=["POST"])
def registration():
    db_sess = db_session.create_session()
    params = request.json
    user = User(
        name=params['name'],
        email=params['email'],
    )
    user.set_password(params['password'])
    db_sess.add(user)
    db_sess.commit()
    token = user.get_token()
    return {'access_token': token}


@app.route('/login', methods=['POST'])
def login():
    db_sess = db_session.create_session()
    params = request.json
    user = db_sess.query(User).filter(params['email'] == User.email).one()
    if not user.check_password(params['password']):
        raise Exception('No user with this password')
    token = user.get_token()
    return {'access_token': token}


def main():
    db_session.global_init('db/data_of_users.db')
    app.run()


if __name__ == '__main__':
    main()
