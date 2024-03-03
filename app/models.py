from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import create_access_token
from flask_bcrypt import Bcrypt
import jwt
from extensions import db
# Create the database models.
 
class Flower(db.Model):
    __tablename__ = 'flower'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    sku = db.Column(db.String(100), unique=True, nullable=False)
    category = db.Column(db.String(100), nullable=False)
    active = db.Column(db.Boolean, default=True)
    description = db.Column(db.Text, nullable=True)
    show_on_site = db.Column(db.Boolean, default=False)
    image = db.Column(db.String(100), nullable=True)

    price_40 = db.Column(db.Float, nullable=True)
    quantity_40 = db.Column(db.Integer, nullable=True)
    add_to_bouquet_40 = db.Column(db.Boolean, default=False)

    price_50 = db.Column(db.Float, nullable=True)
    quantity_50 = db.Column(db.Integer, nullable=True)
    add_to_bouquet_50 = db.Column(db.Boolean, default=False)

    price_60 = db.Column(db.Float, nullable=True)
    quantity_60 = db.Column(db.Integer, nullable=True)
    add_to_bouquet_60 = db.Column(db.Boolean, default=False)

    price_70 = db.Column(db.Float, nullable=True)
    quantity_70 = db.Column(db.Integer, nullable=True)
    add_to_bouquet_70 = db.Column(db.Boolean, default=False)

    price_80 = db.Column(db.Float, nullable=True)
    quantity_80 = db.Column(db.Integer, nullable=True)
    add_to_bouquet_80 = db.Column(db.Boolean, default=False)

    price_90 = db.Column(db.Float, nullable=True)
    quantity_90 = db.Column(db.Integer, nullable=True)
    add_to_bouquet_90 = db.Column(db.Boolean, default=False)

    price_100 = db.Column(db.Float, nullable=True)
    quantity_100 = db.Column(db.Integer, nullable=True)
    add_to_bouquet_100 = db.Column(db.Boolean, default=False)

    price_110 = db.Column(db.Float, nullable=True)
    quantity_110 = db.Column(db.Integer, nullable=True)
    add_to_bouquet_110 = db.Column(db.Boolean, default=False)

    sizes = db.relationship('FlowerSize', backref='flower')

class FlowerSize(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    flower_id = db.Column(db.Integer, db.ForeignKey('flower.id'), nullable=False)
    size = db.Column(db.String(20), nullable=False)
    price = db.Column(db.Float, nullable=False)

class Material(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

bouquet_flowers = db.Table('bouquet_flowers',
    db.Column('bouquet_id', db.Integer, db.ForeignKey('bouquet.id'), primary_key=True),
    db.Column('flower_id', db.Integer, db.ForeignKey('flower.id'), primary_key=True)
)

bouquet_materials = db.Table('bouquet_materials',
    db.Column('bouquet_id', db.Integer, db.ForeignKey('bouquet.id'), primary_key=True),
    db.Column('material_id', db.Integer, db.ForeignKey('material.id'), primary_key=True),
    db.Column('quantity', db.Integer, nullable=False),
    db.Column('price', db.Float, nullable=False)
)

class Bouquet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=False, nullable=False)
    sku = db.Column(db.String(20), unique=True, nullable=False)  # SKU - уникальный идентификатор товара
    category = db.Column(db.String(20), nullable=False)  # Категория букета: базовый цветок или букет
    active = db.Column(db.Boolean, default=True)  # Статус активности товара
    description = db.Column(db.Text)              # Описание товара
    image = db.Column(db.LargeBinary)             # Изображение товара
    show_on_site = db.Column(db.Boolean, default=True)  # Показывать ли букет на сайте
    flowers = db.relationship('Flower', secondary=bouquet_flowers)
    materials = db.relationship('Material', secondary=bouquet_materials)
    
    def calculate_price(self, specific_size=None):
        if specific_size:
            # Calculate price for a specific size
            return self.calculate_price_for_size(specific_size)
        else:
            # Calculate price for all sizes
            return self.calculate_price_all_sizes()

    def calculate_price_for_size(self, size):
        total_price = 0
        for bouquet_flower in self.flowers:  # Assuming 'flowers' is a relationship
            for flower_size in bouquet_flower.flower.sizes:
                if flower_size.size == size:
                    total_price += flower_size.price * bouquet_flower.quantity
                    break
        return total_price

    def calculate_price_all_sizes(self):
        size_prices = {}
        for bouquet_flower in self.flowers:
            for flower_size in bouquet_flower.flower.sizes:
                if flower_size.size not in size_prices:
                    size_prices[flower_size.size] = 0
                size_prices[flower_size.size] += flower_size.price * bouquet_flower.quantity
        return size_prices

class BouquetFlower(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    bouquet_id = db.Column(db.Integer, db.ForeignKey('bouquet.id'), nullable=False)
    flower_id = db.Column(db.Integer, db.ForeignKey('flower.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

class BouquetMaterial(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    bouquet_id = db.Column(db.Integer, db.ForeignKey('bouquet.id'), nullable=False)
    material_id = db.Column(db.Integer, db.ForeignKey('material.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)
    
db.create_all