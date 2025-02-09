from app.extentions import db
from werkzeug.security import generate_password_hash, check_password_hash 
from flask_login import UserMixin

class Restaurant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    location = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    telephone = db.Column(db.String(15), nullable=False, unique=True)

    def __repr__(self):
        return f'<Restaurant {self.name}>'

    def __init__(self, name, location, email, telephone):
        self.name = name
        self.location = location
        self.email = email
        self.telephone = telephone





class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)

    # Add the is_active_user column
    is_active_user = db.Column(db.Boolean, default=True)  # This will be used to track if the user is active


    # Hash and store the password
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    # Check if the provided password matches the stored hash
    def check_password(self, password):
        return check_password_hash(self.password_hash, password) 
    
    def is_active(self):
        """Returns true if the user ia active, false if not"""
        return self.is_active_user
    
    def __repr__(self):
        return f"<User {self.username}>"
    
    # def get_id(self):
    #     """ Returns the unique user ID as a string (required by Flask-Login) """
    #     return str(self.id)  # Flask-Login requires ID as a string
    
    """def is_authenticated(self):
    # return True""" 