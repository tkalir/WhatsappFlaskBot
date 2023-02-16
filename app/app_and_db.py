from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, static_folder='public', template_folder='views')
db_url = "/.data/dreams.db"
#app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite://{}".format(db_url)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///:memory:"
db = SQLAlchemy(app)