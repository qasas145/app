from flask import Flask, jsonify, make_response, request
from flask_cors import CORS
import os


app = Flask(__name__)


CORS(app)

base_dir = os.path.dirname(os.path.realpath(__file__))

app.config['SECRET_KEY'] = 'ahmed'
app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.path.join(base_dir, 'databases/user.db')
app.config['SQLALCHEMY_ECHO'] = True
