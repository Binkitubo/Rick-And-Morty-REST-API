"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for, json
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Character, Location, favorites
from models import Character
from models import Location
from models import favorites

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/characters', methods=['GET', 'POST'])
def get_create_characters():
    
    if request.method == 'GET':
        character = Character.query.all()
        characters_list = list(map(lambda character: character.serialize(), character))
    
        return jsonify(characters_list), 200
    
    else:
        body = request.get_json()
        
        character = Character()
        character.name = body['name']
        character.status = body['status']
        character.species = body['species']
        character.gender = body['gender']
        character.origin = body['origin']
        
        db.session.add(character)
        db.session.commit()
        
        response_body = {
            "created": True,
            "character": character.serialize()
        }
        
        return jsonify(response_body), 201

@app.route('/characters/<int:character_id>', methods=['GET'])
def get_single_character(character_id):
    character = Character.query.get(character_id)    
    
    return jsonify(character.serialize()), 200

@app.route('/characters/<int:character_id>', methods=['PUT', 'DELETE'])
def edit_delete_character(character_id):
    body = request.get_json()
    update_character = Character.query.get(character_id)
    
    if request.method == 'PUT':
        
        if 'name' in body:
            update_character.name = body['name']
        if 'status' in body:
            update_character.status = body['status']
        if 'species' in body:
            update_character.species = body['species']
        if 'gender' in body:
            update_character.gender = body['gender']
        if 'origin' in body:
            update_character.origin = body['origin']
            
        db.session.commit()
        
        response_body = {
            "modified": True,
            "character": update_character.serialize()
        }
        
        return jsonify(response_body), 200
    
    else:                
        db.session.delete(update_character)
        db.session.commit()
        
        character = Character.query.all()
        characters_list = list(map(lambda character: character.serialize(), character))
        
        response_body = {
            "deleted": True,
            "characters": characters_list
        }
               
        return jsonify(response_body), 200
        
@app.route('/locations', methods=['GET', 'POST'])
def get_create_locations():
    
    if request.method == 'GET':
        location = Location.query.all()
        locations_list = list(map(lambda location: location.serialize(), location))
    
        return jsonify(locations_list), 200
    
    else:
        body = request.get_json()
        
        location = Location()
        location.name = body['name']
        location.dimension = body['dimension']
        
        db.session.add(location)
        db.session.commit()
        
        response_body = {
            "created": True,
            "location": location.serialize()
        }
        
        return jsonify(response_body), 201

@app.route('/locations/<int:location_id>', methods=['GET'])
def get_single_location(location_id):
    location = Location.query.get(location_id)
    
    return jsonify(location.serialize()), 200

@app.route('/locations/<int:location_id>', methods=['PUT', 'DELETE'])
def edit_delete_location(location_id):
    body = request.get_json()
    update_location = Location.query.get(location_id)
    
    if request.method == 'PUT':
        if 'name' in body:
            update_location.name = body['name']
        if 'dimension' in body:
            update_location.dimension = body['dimension']
        
        db.session.commit()
        
        response_body = {
            "modified": True,
            "location": update_location.serialize()
        }
        
        return jsonify(response_body), 200
    
    else:
        db.session.delete(update_location)
        db.session.commit()
        
        location = Location.query.all()
        locations_list = list(map(lambda location: location.serialize(), location))
        
        response_body = {
            "deleted": True,
            "locations": locations_list
        }
        
        return jsonify(response_body), 200

@app.route('/user', methods=['GET', 'POST'])
def get_create_user():
    
    if request.method == 'GET':
        user = User.query.all() 
        user_list = list(map(lambda user : user.serialize(), user))
        
        return jsonify(user_list), 200
        
    else:
        body = request.get_json()
        
        user = User()
        user.username = body['username']
        user.email = body['email']
        user.password = body['password']
        user.is_active = body['is_active']
        
        db.session.add(user)
        db.session.commit()
        
        response_body = {
            "created": True,
            "user": user.serialize()
        }
    
    return jsonify(response_body), 201

@app.route('/user/<int:user_id>', methods=['GET'])
def get_single_user(user_id):
    user = User.query.get(user_id)
    
    return jsonify(user.serialize()), 200

@app.route('/user/<int:user_id>/favorite/character/<int:character_id>', methods=['POST', 'GET'])
def add_fav_char(user_id, character_id):
    body = request.get_json()
    user = User.query.get(user_id)
    
    if request.method == 'POST':  
        character = Character.query.get(character_id)
        fav_char = favorites(user_id=user_id, character_id=character_id)
        
        db.session.add(fav_char)
        db.session.commit()
        
        response_body = {
            "is_fav": True,
            "favorites": fav_char.serialize(),
            "user": user.username
        }
        
        return jsonify(response_body), 201
    
    else:        
        favorites = favorites.query.filter_by(user_id=user_id).all()
        all_characters = list(map(lambda character: character.serialize(), favorites))
        
        response_body = {
            "favorites": all_characters,
            "user": user.username
        }
        
        return jsonify(response_body), 200

@app.route('/user/<int:user_id>/favorite/character/<int:character_id>', methods=['DELETE'])
def delete_fav_char(user_id, character_id):
    body = request.get_json()
    user = User.query.get(user_id)
    character = Character.query.get(character_id)
    favorites = favorites.query.filter_by(user_id=user_id, character_id=character_id).first()
    
    db.session.delete(favorites)
    db.session.commit()
    
    response_body = {
        "is_fav": False,
        "user": user.username
    }
    
    return jsonify(response_body), 200

@app.route('/user/<int:user_id>/favorite/location/<int:location_id>', methods=['POST', 'GET'])      
def add_fav_loc(user_id, location_id):
    body = request.get_json()      
    user = User.query.get(user_id)

    if request.method == 'POST':
        location = Location.query.get(location_id)
        fav_loc = favorites(user_id=user_id, location_id=location_id)
        print(fav_loc)
        
        db.session.add(fav_loc)
        db.session.commit()
        
        response_body = {
            "is_fav": True,
            "favorites": fav_loc.serialize(),
            "user": user.username
        }
        
        return jsonify(response_body), 200
    
    else:
        favorites = favorites.query.filter_by(user_id=user_id).all()
        all_locs = list(map(lambda location: location.serialize(), favorites))

        response_body = {
            "favorites": all_locs,
            "user": user.username
        }
        
        return jsonify(response_body), 200

@app.route('/user/<int:user_id>/favorite/location/<int:location_id>', methods=['DELETE'])
def delete_fav_loc(user_id, location_id):
    body = request.get_json()
    user = User.query.get(user_id)
    location = Location.query.get(location_id)
    favorites = favorites.query.filter_by(user_id=user_id, location_id=location_id).first()
  
    db.session.delete(favorites)
    db.session.commit()
    
    response_body = {
        "is_fav": False,
        "user": user.username
    }
    
    return jsonify(response_body), 200

@app.route('/user/<int:user_id>/favorites', methods=['GET'])
def get_all_favs(user_id):
    body = request.get_json()
    user = User.query.get(user_id)
    favorites = favorites.query.filter_by(user_id=user_id)
    all_favs = list(map(lambda favorites:favorites.serialize(),favorites))
    
    response_body = {
        "user": user.username,
        "favorites": all_favs
    }

    return jsonify(response_body), 200

# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
