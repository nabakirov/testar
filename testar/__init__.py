from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()




from config import Config

app = Flask(Config.APP_NAME)
app.config.from_object(Config)

db.init_app(app)







from . import models
from . import views