from main import db, create_app
from flask import  redirect, request, jsonify, url_for, render_template
from models import Flower, Material, Bouquet, FlowerSize, BouquetFlower, BouquetMaterial, Bouquet, db
app = create_app()


def create_bouquet():
    if request.method == 'POST':
        # Process the submitted form data
        selected_flowers = []
        for key in request.form.keys():
            if key.startswith('flower_'):
                flower_id, size_id = key.split('_')[1], key.split('_')[3]
                quantity = request.form[key]
                selected_flowers.append((flower_id, size_id, quantity))

        # Create a new bouquet object
        new_bouquet = Bouquet(name="Custom Bouquet")
        db.session.add(new_bouquet)

        # Add selected flowers to the bouquet
        for flower_id, size_id, quantity in selected_flowers:
            bouquet_flower = BouquetFlower(bouquet_id=new_bouquet.id, flower_id=flower_id, size_id=size_id, quantity=quantity)
            db.session.add(bouquet_flower)

        db.session.commit()

        return redirect(url_for('view_bouquet', bouquet_id=new_bouquet.id))
    else:
        # Display the bouquet creation form
        flowers = Flower.query.all()
        return render_template('create_bouquet.html', flowers=flowers)
    
@app.route('/view_bouquet/<int:bouquet_id>', methods=['GET'])
def view_bouquet(bouquet_id):
    bouquet = Bouquet.query.get_or_404(bouquet_id)
    bouquet_prices = bouquet.calculate_price()  # For all sizes
    # bouquet_prices = bouquet.calculate_price(specific_size="40cm")  # For a specific size
    return render_template('view_bouquet.html', bouquet=bouquet, bouquet_prices=bouquet_prices)


# Get all flowers.
@app.route('/api/flowers', methods=['GET'])
def get_flowers():
    flowers = Flower.query.all()
    return jsonify([{'id': flower.id, 'name': flower.name, 'size': flower.size, 'quantity': flower.quantity} for flower in flowers])

# Create a flower.
@app.route('/api/flowers', methods=['POST'])
def create_flower():
    data = request.get_json()
    new_flower = Flower(name=data['name'], size=data['size'], quantity=data['quantity'])
    db.session.add(new_flower)
    db.session.commit()
    return jsonify({'message': 'Flower created successfully'}), 201

# Get all materials.
@app.route('/api/materials', methods=['GET'])
def get_materials():
    materials = Material.query.all()
    return jsonify([{'id': material.id, 'name': material.name, 'quantity': material.quantity} for material in materials])

# Create a material.
@app.route('/api/materials', methods=['POST'])
def create_material():
    data = request.get_json()
    new_material = Material(name=data['name'], quantity=data['quantity'])
    db.session.add(new_material)
    db.session.commit()
    return jsonify({'message': 'Material created successfully'}), 201

# Get all bouquets.
@app.route('/api/bouquets', methods=['GET'])
def get_bouquets():
    bouquets = Bouquet.query.all()
    return jsonify([{'id': bouquet.id, 'name': bouquet.name, 'flowers': [flower.name for flower in bouquet.flowers], 'materials': [material.name for material in bouquet.materials]} for bouquet in bouquets])

# Create a bouquet.
@app.route('/api/bouquets', methods=['POST'])
def create_bouquet():
    data = request.get_json()
    new_bouquet = Bouquet(name=data['name'])
    for flower in data['flowers']:
        flower_obj = Flower.query.filter_by(name=flower).first()
        new_bouquet.flowers.append(flower_obj)
    for material in data['materials']:
        material_obj = Material.query.filter_by(name=material).first()
        new_bouquet.materials.append(material_obj)
    db.session.add(new_bouquet)
    db.session.commit()
    return jsonify({'message': 'Bouquet created successfully'}), 201

# Get a bouquet by ID.
@app.route('/api/bouquets/<int:bouquet_id>', methods=['GET'])
def get_bouquet(bouquet_id):
    bouquet = Bouquet.query.get(bouquet_id)
    return jsonify({'id': bouquet.id, 'name': bouquet.name, 'flowers': [flower.name for flower in bouquet.flowers], 'materials': [material.name for material in bouquet.materials]})

# Update a bouquet.
@app.route('/api/bouquets/<int:bouquet_id>', methods=['PUT'])
def update_bouquet(bouquet_id):
    data = request.get_json()
    bouquet = Bouquet.query.get(bouquet_id)
    bouquet.name = data['name']
    for flower in data['flowers']:
        flower_obj = Flower.query.filter_by(name=flower).first()
        bouquet.flowers.append(flower_obj)
    for material in data['materials']:
        material_obj = Material.query.filter_by(name=material).first()
        bouquet.materials.append(material_obj)
    db.session.commit()
    return jsonify({'message': 'Bouquet updated successfully'}), 200

# Delete a bouquet.
@app.route('/api/bouquets/<int:bouquet_id>', methods=['DELETE'])
def delete_bouquet(bouquet_id):
    bouquet = Bouquet.query.get(bouquet_id)
    db.session.delete(bouquet)
    db.session.commit()
    return jsonify({'message': 'Bouquet deleted successfully'}), 200