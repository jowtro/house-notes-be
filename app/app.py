import os
from flask import Flask
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from models import db
from models.user_model import UserModel
from routes.api import api
from dotenv import load_dotenv
from flask.cli import AppGroup
import click
from flask_cors import CORS

user_cli = AppGroup('user')

load_dotenv()

app = Flask(__name__, instance_relative_config=True)
app.config.from_object(os.environ["APP_SETTINGS"])
jwt = JWTManager(app)
ma = Marshmallow(app)
# initialize database and track changes
db.init_app(app)
ma.init_app(app)
migrate = Migrate(app, db)
app.register_blueprint(api, url_prefix="/api/v1")
# CORS
cors = CORS(app)
# allow CORS to all routes
#config CORS for specifc origins if you want
app.config['CORS_HEADERS'] = 'Content-Type'



@user_cli.command("create")
@click.option("--username", prompt="Username", help="The username for the user.")
@click.option(
    "--password", prompt="Password", hide_input=True, help="The password for the user."
)
@click.option("--email", prompt="E-mail", help="The e-mail for the user.")
def create_user(username, password, email):
    """Create a new user"""
    new_user = UserModel(username=username, password=password, email=email)
    db.session.add(new_user)
    db.session.commit()
    click.echo(f"User {username} created")
    
app.cli.add_command(user_cli)
