from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
import os.path

class Config():
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(BASE_DIR, "app.db")
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'app.db')
    SQLALCHEMY_COMMIT_ON_TEARDOWN = False # Autocommit
    SQLALCHEMY_TRACK_MODIFICATIONS = False # ??? Если не прописать, то будет Warning
    SECRET_KEY = 'we4fh%gC_za:*8G5v=fbv'


app = Flask(__name__)
app.config.from_object(Config())
db = SQLAlchemy(app=app, session_options={'autoflush': False})
csrf = CSRFProtect(app)