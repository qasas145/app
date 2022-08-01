from .serializers import Resource, UserModel
from .urls import api
from .app import request, make_response, jsonify, app
from .models import User, db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
from .auth import token_required, jwt





class UserData(Resource) :
    @api.marshal_list_with(UserModel, envelope = "users", code = 200)
    @token_required
    @api.doc(security='apikey')
    def get(self, user) :
        users = User.query.all()
        return users

    @api.marshal_with(UserModel, envelope = "user", code = 201)
    @token_required
    @api.doc(params = {"name" : "User name", "age" : "User age", "title" : "User title", 'password' : "User password"}, security='apikey')
    def post(self, user) :
        data = request.args
        keys = ['name', 'age', 'title', 'password']
        check = [True if data.get(key) is not None else False  for key in keys ]
        if not all(check) :
            return {'message' : 'fill the empty fields please .'}, 400
        name = data.get("name")
        try :
            age = int(data.get("age"))
        except :
            return {'message' : 'enter a correct age format .'}, 400 
        title = data.get("title")
        password = data.get('password')
        new_user = User(name = name, age = age, title = title, password = generate_password_hash(password))
        db.session.add(new_user)
        db.session.commit()
        return new_user


class UserDataPk(Resource) :

    
    @token_required
    @api.marshal_with(UserModel, envelope = "user_get", code = 201)
    @api.doc(security='apikey')
    def get(self, user, id):
        user = User.query.get_or_404(id)
        return user
    @token_required
    @api.marshal_with(UserModel, envelope = "user_put", code = 201)
    @api.doc(params={'name' : 'User name', 'age' : 'User age', 'title' : 'User title'}, security='apikey')
    def put(self, user, id)  :
        data = request.args
        user = User.query.get_or_404(id)
        if data.get('name') != None :
            user.name = data.get('name')
        if data.get('age') != None :
            try :
                user.age = int(data.get('age'))
            except :
                pass
        if data.get('title') != None :
            user.title = data.get('title')
        db.session.commit()
        return user


    @token_required
    @api.marshal_with(UserModel, envelope = "user", code = 201)
    @api.doc(security='apikey')
    def delete(self, user, id) :
        user = User.query.get_or_404(id)
        db.session.delete(user)
        db.session.commit()
        return user

class Login(Resource) :
    @api.doc(params = {'id' : 'user id', 'password' : 'user password'}, security = [])
    def post(self) :
        data = request.args
        id = int(data.get('id'))
        password = data.get('password')
        user = User.query.filter_by(id = id).first()
        if not user : 
            return make_response(jsonify('Could not verify',
        403,
        {'WWW-Authenticate' : 'Basic realm ="Wrong Id !!"'}))

        if (check_password_hash(user.password, password)) :
            token = jwt.encode({
            'id': user.id,
            'exp' : datetime.utcnow() + timedelta(hours=1),
            }, app.config['SECRET_KEY'], algorithm="HS256")
            return make_response(jsonify({'token' : token}), 201)
        return make_response(jsonify('Could not verify',
        403,
        {'WWW-Authenticate' : 'Basic realm ="Wrong Password !!"'}))

class Signup(Resource) :
    @api.marshal_with(UserModel, envelope = "signup")
    @api.doc(params = {"name" : "User name", "age" : "User age", "title" : "User title", 'password' : "User password"})
    def post(self) :
        data = request.args
        keys = ['name', 'age', 'title', 'password']
        check = [True if data.get(key) is not None else False  for key in keys ]
        if not all(check) :
            return {'message' : 'fill the empty fields please .'}, 400
        name = data.get("name")
        try :
            age = int(data.get("age"))
        except :
            return {'message' : 'enter a correct age format .'}, 400 
        title = data.get("title")
        password = data.get('password')
        new_user = User(name = name, age = age, title = title, password = generate_password_hash(password))
        db.session.add(new_user)
        db.session.commit()
        return new_user




api.add_resource(UserData, "/users/")
api.add_resource(UserDataPk, "/users/<int:id>")
api.add_resource(Login, "/login/")
api.add_resource(Signup, "/signup/")





if __name__ == "__main__" :
    app.run(debug=True)






# @app.shell_context_processor
# def make_shell_processor() :
#     return {
#         "db" : db,
#         "User" : User
#     }