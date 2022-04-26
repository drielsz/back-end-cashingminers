from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
load_dotenv()
import os 

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY")

from app.routes import *