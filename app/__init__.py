from flask import Flask, url_for, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config.from_object('config.Config')
db = SQLAlchemy(app)

from api import v1
from app import views
