from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
import os
from config import basedir
static_folder = os.path.join(basedir, 'web/static')
template_folder = os.path.join(basedir, 'web/templates')

db = SQLAlchemy()




from config import Config

app = Flask(Config.APP_NAME, static_folder=static_folder, template_folder=template_folder)
app.config.from_object(Config)

db.init_app(app)







from . import models
from . import views