from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
import os
from api import *
from models import *
os.environ['HOST'] = '0.0.0.0'

app = Flask(__name__)
app.register_blueprint(index_page)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///warehouse.db'
db = SQLAlchemy(app)

if __name__ == '__main__':
    app.run(host='0.0.0.0')