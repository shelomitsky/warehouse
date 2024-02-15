# extensions.py
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask import Blueprint, render_template, redirect, request, url_for, flash
from flask_migrate import Migrate
from sqlalchemy.exc import IntegrityError
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, BooleanField, TextAreaField, DecimalField, FloatField
from wtforms.validators import DataRequired, ValidationError
from flask_bootstrap import Bootstrap

db = SQLAlchemy()
login_manager = LoginManager()
bcrypt = Bcrypt()
migrate = Migrate()
bootstrap = Bootstrap()
