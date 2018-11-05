from flask import Blueprint
from flask_restful import Api
from resources.Service import Service
from resources.Service import Service2

api_bp = Blueprint('api', __name__)
api = Api(api_bp)

api.add_resource(Service, '/Service')
api.add_resource(Service2, '/Service2')