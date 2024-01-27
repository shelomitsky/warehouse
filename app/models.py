from flask_sqlalchemy import SQLAlchemy
import jwt
# Create the database models.
db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

    def generate_token(self):
        # Generate a JSON Web Token (JWT) for authentication.
        return jwt.encode({'id': self.id, 'username': self.username}, 'secret', algorithm='HS256')

class Flower(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    size = db.Column(db.String(20), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)
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

class Bouquet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    flowers = db.relationship('Flower', secondary='bouquet_flowers')
    materials = db.relationship('Material', secondary='bouquet_materials')
    
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