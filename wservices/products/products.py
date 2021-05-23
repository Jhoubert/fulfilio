import json

import sqlalchemy
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required

from database import db_session
from models import Product
from schemas import CreateProductSchema, ProductSchema, UpdateProductSchema

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


@products.route('/update/<int:id>', methods=['POST'])
@jwt_required()
def update(id):
    """
    ---
    post:
      description: Update an existing entry in the database, all fields are optionals, if you send only name it will update only name
      requestBody:
        required: true
        content:
          'application/json':
           schema: UpdateProductSchema
      responses:
        '200':
          description: Successful call.
          content:
            application/json:
              schema: ProductSchema
        '401':
          description: Does't have permissions to update a product.
        '409':
          description: sku already exists
        '400':
          description: Invalid json body request or missing values.
        '404':
          description: Product not found
      parameters:
        - name: Authorization
          in: header
          description: JWT authorization header
          required: true
          type: string
      tags:
          - Products
    """

    data_schema = UpdateProductSchema()
    validations = data_schema.validate(request.json)

    if len(validations.keys()) > 0:
        return jsonify({"msg": "Invalid json body request or missing values."}), 400
    data_schema.loads(json.dumps(request.json))

    update_product = db_session.query(Product).filter(Product.id == id).first()

    for key, value in request.json.items():
        if hasattr(update_product, key):
            setattr(update_product, key, value)

    try:
        db_session.commit()
    except sqlalchemy.exc.IntegrityError as e:
        if "duplicate key value violates unique constraint" in str(e):
            return jsonify({"msg": "SKU already exists"}), 409
        else:
            return jsonify({"msg": "Service unavailable, unknown db error."}), 503

    sch = ProductSchema()
    return jsonify(sch.dump(update_product))


@products.route('/delete/<int:id>', methods=['DELETE'])
@jwt_required()
def delete(id):
    """
    ---
    delete:
      description: Delete a product in the url
      responses:
        '200':
          description: Successfully deleted
          content:
            application/json:
              schema: ActionOutputSchema
        '401':
          description: Does't have permissions to delete.
        '404':
          description: Product not found
      parameters:
        - name: Authorization
          in: header
          description: JWT authorization header
          required: true
          type: string
      tags:
          - Users
    """

    obj = db_session.query(Product).filter_by(id=id).first()
    if not obj:
        return jsonify({"msg": "User does not exists"}), 404

    try:
        db_session.delete(obj)
        db_session.commit()
    except Exception as e:
        return jsonify({"result": "Error deleting product "+id})
    return jsonify({"result": "success"})


@products.route('/delete_all_products', methods=['DELETE'])
@jwt_required()
def delete_all():
    """
    ---
    delete:
      description: Delete all products from the database
      responses:
        '200':
          description: Successfully deleted
          content:
            application/json:
              schema: ActionOutputSchema
        '401':
          description: Does't have permissions to delete.
      parameters:
        - name: Authorization
          in: header
          description: JWT authorization header
          required: true
          type: string
      tags:
          - Users
    """
    try:
        db_session.query(Product).delete()
        db_session.commit()
    except Exception as e:
        return jsonify({"result": "Error deleting all products"})

    return jsonify({"result": "success"})
