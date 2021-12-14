from flask import Blueprint, request, jsonify
from werkzeug.wrappers import response
from  plant_collection.helpers import token_required
from plant_collection.models import db, User, Plant, plant_schema, plants_schema

api = Blueprint('api', __name__, url_prefix='/api')

@api.route('/getdata')
@token_required
def getdata(current_user_token):
    return{'some' : 'value'}

# Endpoint Route and Function to create a new plant in database
@api.route('/plants', methods=['POST'])
@token_required
def create_plant(current_user_token):
    name = request.json['name']
    room = request.json['room']
    plant_type = request.json['plant_type']
    light = request.json['light']
    description = request.json['description']
    water = request.json['water']
    fertilizer = request.json['fertilizer']
    humidity = request.json['humidity']
    pests = request.json['pests']
    fun_fact = request.json['fun_fact']
    user_token = current_user_token.token

    plant = Plant(name, room, plant_type, light, description, water, fertilizer, humidity, pests, fun_fact, user_token)
    db.session.add(plant)
    db.session.commit()

    response = plant_schema.dump(plant)
    return jsonify(response)

# Endpoint Route and Function to retrieve all plants
@api.route('/plants', methods=['GET'])
@token_required
def get_plants(current_user_token):
    owner = current_user_token.token
    plants = Plant.query.filter_by(user_token = owner).all()
    response = plants_schema.dump(plants)
    return jsonify(response)

# Endpoint Route and Function to retrieve a single plant
@api.route('/plants/<id>', methods=['GET'])
@token_required
def get_plant(current_user_token, id):
    owner = current_user_token.token
    if owner == current_user_token.token:
        plant = Plant.query.get(id)
        response = plant_schema.dump(plant)
        return jsonify(response)
    else:
        return jsonify({'message' : 'Valid Token Required'}),401

# Endpoint Route and Function to update a plant
@api.route('/plants/<id>', methods = ['POST', 'PUT'])
@token_required
def update_plant(current_user_token, id):
    plant = Plant.query.get(id)
    plant.name = request.json['name']
    plant.room = request.json['room']
    plant.plant_type = request.json['plant_type']
    plant.light = request.json['light']
    plant.description = request.json['description']
    plant.water = request.json['water']
    plant.fertilizer = request.json['fertilizer']
    plant.humidity = request.json['humidity']
    plant.pests = request.json['pests']
    plant.fun_fact = request.json['fun_fact']
    plant.user_token = current_user_token.token

    db.session.commit()
    response = plant_schema.dump(plant)
    return jsonify(response)

# Endpoint Route and Funtion to delete a plant
@api.route('/plants/<id>', methods = ['DELETE'])
@token_required
def delete_plant(current_user_token, id):
    plant = Plant.query.get(id)
    print(plant)

    db.session.delete(plant)
    db.session.commit()
    response = plant_schema.dump(plant)
    return jsonify(response)