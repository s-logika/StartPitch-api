from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_jwt_extended import JWTManager

bcrypt = Bcrypt()
jwt = JWTManager()
cors = CORS()
