from flask import Flask
from marshmallow import Schema, fields, pre_load, validate
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy


ma = Marshmallow()
db = SQLAlchemy()


class Asignar(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    num = db.Column(db.Integer, nullable=False)
    json = db.Column(db.JSON)

    def __init__(self, num, id, json):
        self.num = num
        self.id = id
        self.json = json
