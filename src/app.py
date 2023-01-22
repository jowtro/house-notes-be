import os
from flask import Flask
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from src.models.note_model import db
from src.routes.api import api
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__, instance_relative_config=True)
app.config.from_object(os.environ["APP_SETTINGS"])
ma = Marshmallow(app)
# initialize database and track changes
db.init_app(app)
ma.init_app(app)
migrate = Migrate(app, db)
app.register_blueprint(api, url_prefix="/api/v1")