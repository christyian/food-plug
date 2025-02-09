from flask import Flask #url_for
from app.home import home
from app.auth import auth
from app.extentions import db
from flask_migrate import Migrate
from flask_login import LoginManager


migrate = Migrate()



def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = "mysecret_key"

    db.init_app(app)
    migrate.init_app(app, db)  # Initialize Flask-Migrate with app and db
    login_manager = LoginManager(app)
    login_manager.login_view = "auth.log_in"  # Redirects unauthorized users to login page


    # Import models AFTER db is initialized to avoid circular import issues
    from .models import User  

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    app.register_blueprint(home, url_prefix="")
    app.register_blueprint(auth, url_prefix="")
    

    return app

app = create_app()