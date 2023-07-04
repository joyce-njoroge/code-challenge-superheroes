#!/usr/bin/env python3

from flask import Flask, make_response, jsonify, abort, request
from flask_migrate import Migrate

from models import db, Hero, Power, HeroPower

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/heroes', methods=['GET'])
def get_heroes():
    heroes = Hero.query.all()
    hero_data = [
        {
            'id': hero.id,
            'name': hero.name,
            'super_name': hero.super_name
        }
        for hero in heroes
    ]
    return jsonify(hero_data)

@app.route('/heroes/<int:id>', methods=['GET'])
def hero_by_id(id):
    hero = Hero.query.get(id)
    if hero is None:
        return jsonify({"error": "Hero not found"}), 404

    powers = [
        {
            'id': power.id,
            'name': power.name,
            'description': power.description
        }
        for power in hero.powers
    ]

    hero_data = {
        'id': hero.id,
        'name': hero.name,
        'super_name': hero.super_name,
        'powers': powers
    }
    return jsonify(hero_data)

@app.route('/powers', methods=['GET'])
def get_powers():
    powers = Power.query.all()
    power_data = [
        {
            'id': power.id,
            'name': power.name,
            'description': power.description
        }
        for power in powers
    ]
    return jsonify(power_data)

@app.route('/powers/<int:id>', methods=['GET'])
def power_by_id(id):
    power = Power.query.get(id)
    if power is None:
        return jsonify({"error": "Power not found"}), 404

    power_data = {
        'id': power.id,
        'name': power.name,
        'description': power.description
    }
    return jsonify(power_data)

@app.route('/powers/<int:id>', methods=['PATCH'])
def update_power(id):
    power = Power.query.get(id)
    if power is None:
        return jsonify({"error": "Power not found"}), 404

    description = request.json.get('description')
    if description is not None:
        # Perform validation on power.description
        try:
            Power.validate_description(None, 'description', description)
        except ValueError as e:
            return jsonify({"errors": [str(e)]}), 400

        power.description = description

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"errors": ["Validation errors"]}), 400

    power_data = {
        'id': power.id,
        'name': power.name,
        'description': power.description
    }
    return jsonify(power_data)

@app.route('/hero_powers', methods=['POST'])
def create_hero_power():
    data = request.get_json()
    strength = data.get('strength')
    power_id = data.get('power_id')
    hero_id = data.get('hero_id')

    if hero_id is None or power_id is None or strength is None:
        response = {
            'errors': ['Missing required fields']
        }
        return jsonify(response), 400

    hero = Hero.query.get(hero_id)
    power = Power.query.get(power_id)

    if hero is None or power is None:
        response = {
            'errors': ['Hero or power not found']
        }
        return jsonify(response), 404
    hero_power = HeroPower(strength=strength, power=power, hero=hero)
    db.session.add(hero_power)
    db.session.commit()

    # Retrieve the data related to the Hero
    hero_data = {
        'id': hero.id,
        'name': hero.name,
        'super_name': hero.super_name,
        'powers': [{'id': p.id, 'name': p.name, 'description': p.description} for p in hero.powers]
    }

    response = jsonify(hero_data)
    return response, 200

@app.route('/')
def home():
    return 'Hello World'


if __name__ == '__main__':
    app.run(port=5555)
