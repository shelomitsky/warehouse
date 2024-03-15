# extensions.py
from flask_sqlalchemy import SQLAlchemy
from flask_login import login_user, login_required, logout_user, current_user, UserMixin, LoginManager
from flask_bcrypt import Bcrypt
from flask import Blueprint, render_template, redirect, request, url_for, flash, session
from flask_migrate import Migrate
from sqlalchemy.exc import IntegrityError
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, SelectField, BooleanField, TextAreaField, DecimalField, FloatField, SubmitField, SelectMultipleField, IntegerField, validators, PasswordField
from wtforms.validators import DataRequired, ValidationError, Optional
from flask_bootstrap import Bootstrap5
import logging
import requests

db = SQLAlchemy()
login_manager = LoginManager()
bcrypt = Bcrypt()
migrate = Migrate()
bootstrap = Bootstrap5()
