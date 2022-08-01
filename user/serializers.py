from flask_restx import Api, Resource, fields
from flask import Flask
from app import app




authorization = {
    'apikey' : {
        'type' : 'apiKey',
        'in' : 'header',
        'name' : 'x-access-token'
    }
}


api = Api(app, doc = "/", title="User's API", description="a simple REST API for user data", authorizations=authorization, security='apiKey')



UserModel = api.model(
    "User", {
        'id' : fields.Integer(),
        'name' : fields.String(),
        'age' : fields.Integer(),
        'title' : fields.String(),
    }
)
