from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False) 
    favorites = db.relationship('favorites', backref='User', lazy=True)

    def __repr__(self):
        return '<User %r>' % self.id

    def serialize(self): # do not serialize the password, its a security breach
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "is_active": self.is_active            
        }
        
class Character(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    status = db.Column(db.String(80), nullable=False)
    species = db.Column(db.String(80), unique=False, nullable=False)
    gender = db.Column(db.String(80), unique=False, nullable=False)
    origin = db.Column(db.String(80), unique=False, nullable=False)     
        
    def __repr__(self):
        return '<Character %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "status": self.status,
            "species": self.species,
            "gender": self.gender,
            "origin": self.origin,
        }        
        
class Location(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    dimension = db.Column(db.String(80), unique=False, nullable=False)

    def __repr__(self):
        return '<Location %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "dimension": self.dimension,
        }
        
class favorites(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    character_id = db.Column(db.Integer, db.ForeignKey('character.id'))
    location_id = db.Column(db.Integer, db.ForeignKey('location.id'))
    
    def __repr__(self):
        return '<favorites %r>' % self.id

    def serialize(self):
        return {
            "user_id": self.user_id,
            "character_id": self.character_id,
            "location_id": self.location_id,
        }                      