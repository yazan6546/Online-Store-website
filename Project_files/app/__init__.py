from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object(Config)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///your-database.db'  # Replace with your actual database URI

db = SQLAlchemy(app)

# print(db)
# migrate = Migrate(app, db)

from app import route
