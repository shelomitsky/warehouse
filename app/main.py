from flask import Flask, render_template, redirect, request
from flask_sqlalchemy import SQLAlchemy
import os
from extensions import *
from auth.auth import User, bl_login
from admin.admin import admin
from sync.sync_stat import oc_sync
from models import *

os.environ['HOST'] = '0.0.0.0'
os.environ['FLASK_DEBUG'] = '1'


def create_app():
    
    app = Flask(__name__)
    Bootstrap5(app)
    #configs
    app.secret_key = 'ae1fd358c7612a02fdc6d923fd40308ebefb0e954c7ddb6f9a8bcdd1f3b00c3b'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://warehouse:password@dwhdb:5432/warehouse'
    #inits
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.login_view = 'login.login'
    login_manager.init_app(app)

    bcrypt.init_app(app)
    #blueprints
    with app.app_context():
        db.create_all()
    return app 
app = create_app()
  # Укажите вид, используемый для авторизации
app.register_blueprint(bl_login, url_prefix='/auth')
app.register_blueprint(admin, url_prefix='/admin')
app.register_blueprint(oc_sync, url_prefix='/sync')

@login_manager.user_loader
def load_user(user_id):
    return AppUser.query.get(int(user_id))


@app.route('/')
def index():
    return render_template('index.html')
@app.errorhandler(404)
def admin_page_not_found(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(error):
    return render_template('500.html'), 500

@app.errorhandler(401)
def unauthorized(error):
    return render_template('401.html'), 401


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)