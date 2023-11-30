from .handlers import Lock_Api
from flask_restful import Api  

def generate_api_routes(app):
    api = Api(app)
    api.add_resource(Lock_Api, '/api')


