#!/usr/bin/env python3

from flask import Flask, request, make_response, jsonify
from flask_restful import Resource, Api
from flask_migrate import Migrate

from models import db, Hero, Power, HeroPower

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///heroes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def home():
    return 'sucessful'

class Heroes(Resource):
    def get(self):
        heroes = []
        for hero in Hero.query.all():
            hero_dict = {
                "id": hero.id,
                "name": hero.name,
                "super_name": hero.super_name
            }
            heroes.append(hero_dict)
        return make_response(jsonify(heroes), 200)

class HeroesId(Resource):
    
    def get(self, id):
        hero = Hero.query.filter(Hero.id == id).first()
        
        if hero:
            hero_dict = {
                "id": hero.id,
                "name": hero.name,
                "super_name": hero.super_name,
                "powers": []
            }

            for hero_power in hero.hero_powers:
                power_dict = {
                    "id": hero_power.power.id,
                    "name": hero_power.power.name,
                    "description": hero_power.power.description
                }
                hero_dict["powers"].append(power_dict)

            return make_response(jsonify(hero_dict), 200)
        else:
            return make_response(jsonify({"error": "Hero not found"}), 404)

class Powers(Resource):
    
    def get(self):
        powers = []
        
        for power in Power.query.all():
            power_dict = {
                "id": power.id,
                "name": power.name,
                "description": power.description
            }
            powers.append(power_dict)
        return make_response(jsonify(powers), 200)

    def post(self):
        data = request.get_json()

        if not all(key in data for key in ['name', 'description']):
            return make_response(jsonify({"errors": ["Missing data fields"]}), 400)

        try:
            new_power = Power(
                name=data.get('name'),
                description=data.get('description')
            )
            db.session.add(new_power)
            db.session.commit()

            return make_response(jsonify(new_power.to_dict()), 201)

        except ValueError as e:
            return make_response(jsonify({"errors": [str(e)]}), 400)

class PowersId(Resource):
    
    def get(self, id):
        power = Power.query.filter(Power.id == id).first()
        
        if power:
            power_dict = {
                "id": power.id, 
                "name": power.name, 
                "description": power.description 
            }
            return make_response(jsonify(power_dict), 200)
        else:
            return make_response(jsonify({"error": "Power not found"}), 404)

    def patch(self, id):
        power = Power.query.filter(Power.id == id).first()
        
        if not power:
            return make_response(jsonify({"error": "Power not found"}), 404)
        
        try:
            data = request.get_json()
            for key, value in data.items():
                setattr(power, key, value)
            db.session.add(power)
            db.session.commit()
            
            power_dict = {
                "id": power.id, 
                "name": power.name, 
                "description": power.description 
            }
            
            return make_response(jsonify(power_dict), 200)
        except ValueError as e:
            return make_response(jsonify({"error": e.args[0]}), 400)

class HeroPower(Resource):
    def post(self):
        data = request.get_json()
        required_fields = ['strength', 'hero_id', 'power_id']
        missing_fields = [field for field in required_fields if field not in data]

        # Validate presence of required fields
        if missing_fields:
            return {"errors": [f"Missing field: {field}" for field in missing_fields]}, 400

        # Validate 'strength' value
        if data['strength'] not in ['Strong', 'Weak', 'Average']:
            return {"errors": ["validation errors"]}, 400

        try:
            # Validate existence of Hero and Power
            hero = db.session.get(Hero, data['hero_id']) 
            power = db.session.get(Power, data['power_id'])  

            if not hero or not power:
                return {"errors": ["Invalid 'hero_id' or 'power_id'"]}, 400

            # Creation of new HeroPower
            new_hero_power = HeroPower(
                strength=data['strength'],
                hero_id=data['hero_id'],
                power_id=data['power_id']
            )
            db.session.add(new_hero_power)
            db.session.commit()

            # Serialize the new HeroPower along with related Hero and Power
            response_data = {
                'id': new_hero_power.id,
                'strength': new_hero_power.strength,
                'hero_id': new_hero_power.hero_id,
                'power_id': new_hero_power.power_id,
                'hero': hero.to_dict(rules=('-hero_powers.hero',)),
                'power': power.to_dict(rules=('-hero_powers.power',))
            }

            return response_data, 201  # Change to 201 for resource creation

        except Exception as e:
            db.session.rollback()
            print("Error occurred:", e)  # Print error for debugging
            return {"errors": ["An error occurred while creating HeroPower"]}, 500



api.add_resource(Heroes, '/heroes')
api.add_resource(HeroesId, '/heroes/<int:id>')
api.add_resource(Powers, '/powers') 
api.add_resource(PowersId, '/powers/<int:id>', methods=['GET', 'PATCH'])
api.add_resource(HeroPower, '/heropowers', methods=['POST'])

if __name__ == '__main__':
    app.run(debug=True, port=5555)
