from flask_sqlalchemy import SQLAlchemy
from flask_login import login_user, login_required, logout_user, current_user, UserMixin, LoginManager
from flask_jwt_extended import create_access_token
from flask import request, jsonify, url_for
from logging import getLogger
import jwt
from extensions import db, login_manager, bcrypt, Blueprint, render_template, redirect
from admin.admin import admin


auth_blueprint = Blueprint('auth', __name__)
bl_login = Blueprint ('login', __name__)
test_pages = Blueprint('test_pages', __name__)
hashery = Blueprint('hashery',__name__ )
""" Начало авторизации """
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

    def generate_token(self):
        # Генерируем JSON Web Token (JWT) для аутентификации пользователя
        payload = {
            'id': self.id,
            'username': self.username
        }
        token = jwt.encode(payload, 'secret', algorithm='HS256')
        return token
    
    def is_authenticated(self):
        # Здесь вы можете реализовать проверку авторизации на основе токена
        # Возвращайте True, если пользователь авторизован, и False в противном случае
        return True  # Замените на вашу реализацию
    def get_id(self):
        return str(self.id)
""" Конец авторизации """   
@hashery.route('/hasher', methods=['GET', 'POST'])
# создаем отображение в консоли хеша пароля "1"
def hasher():
    if request.method == 'POST':
        hashed_password = bcrypt.generate_password_hash('1').decode('utf-8')
        # Передаем хешированный пароль в шаблон
        return render_template('hasher.html', hashed_password=hashed_password)
    return render_template('hasher.html')

@bl_login.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        user = User.query.filter_by(username=username).first()

        if user:
            password_from_form = request.form['password']
            
            if bcrypt.check_password_hash(user.password, password_from_form):
                # Пароль верный
                return redirect(url_for('admin.home'))
            else:  
                return render_template('login.html', error="Неверный пароль")
        else:
            return render_template('login.html', error="Пользователь не найден")

    # Если запрос методом GET (первичное отображение формы)
    return render_template('login.html')

@test_pages.route('/test_page', methods=['GET'])
def test_page():
    return render_template('test_page.html')