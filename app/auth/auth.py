from flask_sqlalchemy import SQLAlchemy
from flask_login import login_user, login_required, logout_user, current_user, UserMixin, LoginManager
from flask_jwt_extended import create_access_token
from flask_bcrypt import Bcrypt
from main import app
from flask import  redirect, request, jsonify, url_for, render_template
import jwt
db = SQLAlchemy()
login_manager = LoginManager()
bcrypt = Bcrypt()
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

@app.route('/api/auth', methods=['POST'])
def auth():
    data = request.form
    user = User.query.filter_by(username=data['username']).first()
    if not user or not bcrypt.check_password_hash(user.password, data['password']):
        return jsonify({'message': 'Invalid username or password'}), 401
    access_token = user.generate_token()
    login_user(user)
    return jsonify({'token': access_token}), 200

def create_user():
    data = request.form
    hashed_password = bcrypt.generate_password_hash(data['password'], method='sha256')
    new_user = User(username=data['username'], password=hashed_password)
    db.session.add(new_user)
    db.session.commit()
    return redirect(url_for('login'))