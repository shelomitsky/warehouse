from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import create_access_token
from flask_bcrypt import Bcrypt
import jwt
from extensions import db
class ProductDescription(db.Model):
    id = db.Column(db.Integer, primary_key=True) # Внутренний идентификатор описания
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    language_id = db.Column(db.String(255))
    name = db.Column(db.String(255))
    description = db.Column(db.Text)
    meta_description = db.Column(db.Text)
    meta_keyword = db.Column(db.Text)
    meta_title = db.Column(db.Text)
    tag = db.Column(db.Text)

    product = db.relationship('Product', backref=db.backref('product_descriptions', lazy=True)) # Отношение к продукту имя связи:

class ProductAttribute(db.Model):
    id = db.Column(db.Integer, primary_key=True) # Внутренний идентификатор атрибута
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    attribute_id = db.Column(db.String(255))
    name = db.Column(db.String(255))
    text = db.Column(db.Text)
    attribute_group_id = db.Column(db.String(255))
    language_id = db.Column(db.String(255))

    product = db.relationship('Product', backref=db.backref('product_attributes', lazy=True)) # Отношение к продукту (один-ко-многим)

class ProductOption(db.Model):
    id = db.Column(db.Integer, primary_key=True) # Внутренний идентификатор опции
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    name = db.Column(db.String(255))
    type = db.Column(db.String(255))
    required = db.Column(db.Boolean)
    product_option_id = db.Column(db.String(255))
    option_id = db.Column(db.String(255))

    product = db.relationship('Product', backref=db.backref('product_options', lazy=True)) # Отношение к продукту (один-ко-многим)

class ProductCategory(db.Model):
    id = db.Column(db.Integer, primary_key=True) # Внутренний идентификатор категории
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    category_id = db.Column(db.String(255))
    name = db.Column(db.String(255))
    description = db.Column(db.Text)
    sort_order = db.Column(db.Integer)
    meta_title = db.Column(db.Text)
    meta_description = db.Column(db.Text)
    meta_keyword = db.Column(db.Text)
    language_id = db.Column(db.String(255))

    product = db.relationship('Product', backref=db.backref('product_categories', lazy=True)) # Отношение к продукту (один-ко-многим)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    manufacturer = db.Column(db.String(255), nullable=True)
    sku = db.Column(db.String(255))
    model = db.Column(db.String(255))
    image = db.Column(db.String(255))
    price = db.Column(db.Numeric(10, 4))
    tax_value = db.Column(db.Integer, nullable=True)
    rating = db.Column(db.Integer, nullable=True)
    stock_status = db.Column(db.String(255))
    manufacturer_id = db.Column(db.Integer, nullable=True)
    tax_class_id = db.Column(db.Integer, nullable=True)
    date_available = db.Column(db.Date)
    weight = db.Column(db.Numeric(10, 6), nullable=True)
    weight_class_id = db.Column(db.Integer, nullable=True)
    length = db.Column(db.Numeric(10, 6), nullable=True)
    width = db.Column(db.Numeric(10, 6), nullable=True)
    height = db.Column(db.Numeric(10, 6), nullable=True)
    length_class_id = db.Column(db.Integer, nullable=True)
    subtract = db.Column(db.Boolean, nullable=True)
    sort_order = db.Column(db.Integer)
    status = db.Column(db.Boolean)
    stock_status_id = db.Column(db.Integer, nullable=True)
    date_added = db.Column(db.DateTime)
    date_modified = db.Column(db.DateTime)
    viewed = db.Column(db.Integer, nullable=True)
    reward = db.Column(db.Integer, nullable=True)
    points = db.Column(db.Integer, nullable=True)
    shipping = db.Column(db.Boolean)
    quantity = db.Column(db.Integer)
    currency_id = db.Column(db.Integer, nullable=True)
    currency_code = db.Column(db.String(3))
    currency_value = db.Column(db.Numeric(10, 8))

    # Relationships
    descriptions = db.relationship('ProductDescription', backref='product_desc', lazy=True) # Отношение к описанию (один-ко-многим)
    attributes = db.relationship('ProductAttribute', backref='product_attr', lazy=True) # Отношение к атрибутам (один-ко-многим)
    options = db.relationship('ProductOption', backref='product_opt', lazy=True) # Отношение к опциям (один-ко-многим)
    categories = db.relationship('ProductCategory', backref='product_cat', lazy=True) # Отношение к категориям (один-ко-многим)

    def __repr__(self):
        return f'<Product {self.model}>'