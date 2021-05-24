
from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token, jwt_required

from database import db_session
from models import User
from schemas import LoggedUserSchema, LoginSchema
from flask_cors import CORS

auth = Blueprint(name="user", import_name=__name__)
cors = CORS()
cors.init_app(auth, resources={r"/*": {"origins": "*", "supports_credentials": True}})


@auth.route('/login', methods=['POST', 'OPTIONS'])
def login():
    """
    ---
    post:
      description: User's login
      requestBody:
        required: true
        content:
          'application/json':
           schema: LoginSchema
      responses:
        '200':
          Description: Successful call.
          content:
            application/json:
              schema: LoggedUserSchema
        '401':
          description: Invalid username or password
      tags:
          - Users
    """
    if request.method == 'OPTIONS':
        return {}

    login_sch = LoginSchema()
    validations = login_sch.validate(request.json)
    if len(validations.keys()) > 0:
        print(validations)
        return jsonify({"msg": "Invalid json body request or missing values."}), 400

    user = db_session.query(User).filter(User.user == request.json.get("user")
                                         and User.user == request.json.get("password")).first()

    if not user:
        return jsonify({"msg": "Bad username or password"}), 401

    user_schema = LoggedUserSchema()
    data = user_schema.dump(user)
    data.update({'jwt': create_access_token(identity={'id': user.id, 'username': user.user})})

    return jsonify(data)

