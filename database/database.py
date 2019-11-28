import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from flask import Flask
from flask_sqlalchemy import SQLAlchemy


SQLALCHEMY_DATABASE_URL = (
	f'mysql://{os.environ["mysql_user"]}:'
	f'{os.environ["mysql_password"]}@'
	f'{os.environ["mysql_host"]}/'
	f'{os.environ["mysql_db"]}'
)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URL

db = SQLAlchemy(app)
