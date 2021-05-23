import json

import sqlalchemy
from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token, jwt_required

from database import db_session
from models import Product
from schemas import CreateProductSchema, ProductSchema

products = Blueprint(name="products", import_name=__name__)


@products.route('/create', methods=['POST'])
@jwt_required()
def create():
    """
    ---
    post:
      description: Create a new product entry in the database
      requestBody:
        required: true
        content:
          'application/json':
           schema: CreateProductSchema
      responses:
        '200':
          description: Successful call.
          content:
            application/json:
              schema: ProductSchema
        '401':
          description: Does't have permissions to create entry.
        '400':
          description: Invalid json body request or missing values.
      parameters:
        - name: Authorization
          in: header
          description: JWT authorization header
          required: true
          type: string
      tags:
          - Products
    """

    data_schema = CreateProductSchema()
    validations = data_schema.validate(request.json)

    if len(validations.keys()) > 0:
        return jsonify({"msg": "Invalid json body request or missing values."}), 400

    data_schema.loads(json.dumps(request.json))

    new_product = Product(**request.json)
    db_session.add(new_product)

    try:
        db_session.commit()
    except sqlalchemy.exc.IntegrityError as e:
        return jsonify({"msg": "Service unavailable, unknown db error."}), 503

    sch = ProductSchema()
    return jsonify(sch.dump(new_product))


