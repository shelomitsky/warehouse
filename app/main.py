from flask import Flask, render_template, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_login import login_user, login_required, logout_user, current_user
from flask_jwt_extended import JWTManager
import os
from api import *
from models import *
from auth  import LoginManager
os.environ['HOST'] = '0.0.0.0'

app = Flask(__name__)
app.secret_key = 'ae1fd358c7612a02fdc6d923fd40308ebefb0e954c7ddb6f9a8bcdd1f3b00c3b'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///warehouse.db'
db = SQLAlchemy(app)
jwt = JWTManager(app)
login_manager = LoginManager()
login_manager.login_view = 'login'  # Укажите вид, используемый для авторизации
login_manager.init_app(app)

app.register_blueprint(auth_blueprint)
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def user_is_authenticated():
    token = request.cookies.get('token')  # Получите токен из куки (предполагается, что он хранится в куки)

    if token:
        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
            user_id = payload.get('id')
            # Здесь вы можете добавить дополнительную проверку, если это необходимо
            return True
        except jwt.ExpiredSignatureError:
            pass  # Обработка ошибки истечения срока действия токена
    return False


@app.route('/')
@login_required  # Добавьте этот декоратор для защиты маршрута
def index():
    return redirect('/home')


@app.route('/login')
def login():
    return render_template('login.html')
if __name__ == '__main__':
    app.run(host='0.0.0.0')