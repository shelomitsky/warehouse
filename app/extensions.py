# extensions.py
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask import Blueprint, render_template, redirect, request, url_for, flash, session
from flask_migrate import Migrate
from sqlalchemy.exc import IntegrityError
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, SelectField, BooleanField, TextAreaField, DecimalField, FloatField, SubmitField, SelectMultipleField, IntegerField
from wtforms.validators import DataRequired, ValidationError, Optional
from flask_bootstrap import Bootstrap5
import logging

db = SQLAlchemy()
login_manager = LoginManager()
bcrypt = Bcrypt()
migrate = Migrate()
bootstrap = Bootstrap5()
logging.basicConfig(level=logging.DEBUG)