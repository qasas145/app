from .app import request, jsonify, app
from models import User
import jwt
from functools import wraps
import jwt



def token_required(f) :
    @wraps(f)
    def decorated(*args, **kwargs) :
        token = None
        if 'x-access-token' in request.headers :
            token = request.headers['x-access-token']
        if not token :
            return jsonify({'message' : 'Token Is missing'}), 401
        
        try :
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            user = User.query.filter_by(id = data['id']).first()
        except :
            return jsonify({
                "message" : "invalid Token"
            })
        return f(user, *args, **kwargs)
    return decorated
