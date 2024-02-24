from flask import Flask, render_template, redirect, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import login_user, login_required, logout_user, current_user
from flask_jwt_extended import JWTManager
import os
from extensions import db, login_manager, bcrypt, Blueprint, migrate, Bootstrap5
from auth.auth import auth_blueprint, User, bl_login, test_pages, hashery
from admin.admin import admin
from models import *

os.environ['HOST'] = '0.0.0.0'


def create_app():
    
    app = Flask(__name__)
    Bootstrap5(app)
    #configs
    app.secret_key = 'ae1fd358c7612a02fdc6d923fd40308ebefb0e954c7ddb6f9a8bcdd1f3b00c3b'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://warehouse:password@dwhdb:5432/warehouse'
    #inits
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    bcrypt.init_app(app)
    #blueprints
    with app.app_context():
        db.create_all()
    return app 
app = create_app()
# Setup the JWT Manager to handle tokens
jwt = JWTManager(app)

  # Укажите вид, используемый для авторизации
app.register_blueprint(auth_blueprint, url_prefix='/auth')
app.register_blueprint(bl_login)
app.register_blueprint(test_pages)
app.register_blueprint(hashery, url_prefix='/login')
app.register_blueprint(admin, url_prefix='/admin')

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
def index():
    return render_template('index.html')
@app.errorhandler(404)
def admin_page_not_found(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(error):
    return render_template('500.html'), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)