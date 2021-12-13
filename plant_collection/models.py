from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import uuid
from datetime import datetime
import secrets
from flask_login import LoginManager, UserMixin, login_manager
from flask_marshmallow import Marshmallow

# Adding Flask Security for Passwords
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

login_manager = LoginManager()
ma = Marshmallow

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(db.Model, UserMixin):
    id = db.Column(db.String, primary_key=True)
    first_name = db.Column(db.String(150), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(150), nullable=False)
    password = db.Column(db.String, nullable=False) # change to true if we allow chance to login with linked account
    g_auth_verify = db.Column(db.Boolean, default = False)
    token = db.Column(db.String, default='', unique=True)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    plant = db.relationship('Plant', backref="owner", lazy=True)

    def __init__(self, email, first_name = '', last_name = '', id = '', password = '', token = '', g_auth_verify=False):
        self.id = self.set_id()
        self.first_name = first_name
        self.last_name = last_name
        self.password = self.set_password(password)
        self.email = email
        self.token = self.set_token(24)
        self.g_auth_verify = g_auth_verify

    def set_id(self):
        return str(uuid.uuid4())

    def set_password(self, password):
        self.pw_hash = generate_password_hash(password)
        return self.pw_hash

    def set_token(self, length):
        return secrets.token_hex(length)

    def __repr__(self):
        return f"User { self.email } has been added to the Database."

class Plant(db.Model):
    id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String(100), nullable = False)
    room = db.Column(db.String(100), nullable = True)
    plant_type = db.Column(db.String(100), nullable = True)
    light = db.Column(db.String(100), nullable = True)
    description = db.Column(db.String(100), nullable = True)
    water = db.Column(db.String(100), nullable = True)
    fertilizer = db.Column(db.String(100), nullable = True)
    humidity = db.Column(db.String(100), nullable = True) # maybe change to integer
    pests = db.Column(db.String(100), nullable = True)
    fun_fact = db.Column(db.String(100), nullable = True)
    user_token = db.Column(db.String, db.ForeignKey('user.token'), nullable = False)

    def __init__(self, name, room, plant_type, light, description, water, fertilizer, humidity, pests, fun_fact, user_token, id=""):
        self.id = self.set_id()
        self.name = name
        self.room = room
        self.plant_type = plant_type
        self.light = light
        self.description = description
        self. water = water
        self.fertilizer = fertilizer
        self.humidity = humidity
        self.pests = pests
        self.fun_fact = fun_fact
        self.user_token = user_token

    def __repr__(self):
        return f'The following Plant has been added: {self.name}'