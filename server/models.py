from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
from sqlalchemy_serializer import SerializerMixin


db = SQLAlchemy()

class Hero(db.Model, SerializerMixin):
    __tablename__ = 'heroes'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    super_name = db.Column(db.String)
    
    # Define the relationship to HeroPower
    hero_powers = db.relationship('HeroPower', backref='hero', lazy=True)
    
    serialize_rules = ('-hero_powers.hero',)
    
    def to_dict(self, include_powers=False):
        hero_dict = {
            'id': self.id,
            'name': self.name,
            'super_name': self.super_name,
        }
        if include_powers:
            hero_dict['hero_powers'] = [hp.to_dict() for hp in self.hero_powers]
        return hero_dict

    def __repr__(self):
        return f'<Hero {self.id}: {self.super_name}>'

class Power(db.Model, SerializerMixin):
    __tablename__ = 'powers'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    description = db.Column(db.String)
    
    # Define the relationship to HeroPower
    hero_powers = db.relationship('HeroPower', backref='power', lazy=True)
    
    serialize_rules = ('-hero_powers.power',)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description
        }
    
    @validates('description')
    def validate_description(self, key, body):
        if len(body) < 20:
            raise ValueError('description must be at least 20 characters')
        return body
    
    def __repr__(self):
        return f'<Power {self.id}: {self.name}; {self.description}>'

class HeroPower(db.Model, SerializerMixin):
    __tablename__ = 'hero_powers'
    
    id = db.Column(db.Integer, primary_key=True)
    strength = db.Column(db.String)
    hero_id = db.Column(db.Integer, db.ForeignKey('heroes.id'), nullable=False)
    power_id = db.Column(db.Integer, db.ForeignKey('powers.id'), nullable=False)
    
    serialize_rules = ('-hero.hero_powers', '-power.hero_powers')

    def to_dict(self):
        return {
            'id': self.id,
            'hero_id': self.hero_id,
            'power_id': self.power_id,
            'strength': self.strength,
            'hero': {
                'id': self.hero.id,
                'name': self.hero.name,
                'super_name': self.hero.super_name
            },
            'power': {
                'id': self.power.id,
                'name': self.power.name,
                'description': self.power.description
            }
        }
    
    @validates('strength')
    def validate_strength(self, key, value):
        if value not in ['Strong', 'Weak', 'Average']:
            raise ValueError('Invalid strength')
        return value
    
    def __repr__(self):
        return f'<Hero-Power {self.id}: {self.strength} {self.hero_id} {self.power_id}>'
