from .serializers import api
from views import UserData, UserDataPk, Login, Signup



api.add_resource(UserData, "/users/")
api.add_resource(UserDataPk, "/users/<int:id>")
api.add_resource(Login, "/login/")
api.add_resource(Signup, "/signup/")

