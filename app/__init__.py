from flask import Flask
from flask_restx import Api
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
api = Api()

def create_app():
  
  app = Flask(__name__)
  app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///api.db'

  db.init_app(app)
  api.init_app(app)
  
  from app.controllers.controller import ns
  api.add_namespace(ns, "/Testing")

  return app