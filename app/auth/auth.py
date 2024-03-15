from flask_sqlalchemy import SQLAlchemy
from flask_login import login_user, login_required, logout_user, current_user, UserMixin, LoginManager
from flask import request, jsonify, url_for
from logging import getLogger
from extensions import *
from models import *


bl_login = Blueprint ('login', __name__)
""" Начало авторизации """
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)
    
    def get_id(self):
        return str(self.id)
""" Конец авторизации """   

@bl_login.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        user = AppUser.query.filter_by(username=username).first()

        if user:
            password_from_form = request.form['password']
            if bcrypt.check_password_hash(user.password, password_from_form):
                login_user(user)  # Вход пользователя
                return redirect(url_for('admin.index'))
            else:
                return render_template('login.html', error="Неверный пароль")
        else:
            return render_template('login.html', error="Пользователь не найден")

    return render_template('login.html')  # Возвращает страницу входа при GET запросе


@bl_login.route('/logout')

def logout():
    logout_user()
    return redirect(url_for('login.login'))
