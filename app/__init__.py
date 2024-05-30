from flask import Flask # Create the app
from config import Config # Store configuration
from flask_sqlalchemy import SQLAlchemy # Database interaction
from flask_migrate import Migrate # Handle database migrations
from flask_login import LoginManager # User authentication
from flask_wtf.csrf import CSRFProtect # Protect against Cross-Site Request Forgery attacks

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

login_manager = LoginManager(app)
login_manager.login_view = 'auth.login'

csrf = CSRFProtect(app)

from app.auth import auth
from app.main import main

app.register_blueprint(auth)
app.register_blueprint(main)

