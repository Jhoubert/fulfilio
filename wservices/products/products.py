import csv
import json
import os
from math import ceil

import pandas as pd

import sqlalchemy
from celery import states, Celery
from flask import Blueprint, jsonify, request, make_response, current_app, Flask
from flask_jwt_extended import jwt_required

import config
from database import db_session, engine, init_engine, init_db
from models import Product
from products.importer import insert_data
from schemas import CreateProductSchema, ProductSchema, UpdateProductSchema

from celery.utils.log import get_task_logger

logging = get_task_logger(__name__)

products = Blueprint(name="products", import_name=__name__)
app = Flask(__name__)

app.config.update(
    CELERY_BROKER_URL='amqp://%s' % config.amqp_url,
    CELERY_RESULT_BACKEND='amqp://%s' % config.amqp_url
)

# Database configuration and initialization for celery
if not engine:
    app.config['SQLALCHEMY_DATABASE_URI'] = config.database_string
    init_engine(app.config['SQLALCHEMY_DATABASE_URI'])
    init_db()

celery = Celery(app.name, backend='amqp', broker=app.config['CELERY_BROKER_URL'])


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


@products.route('/upload', methods=['POST'])
def upload():
    file_obj = request.files.get('file')
    file_name = file_obj.filename
    path = os.path.join('./uploads', file_name)
    file_obj.read(0)
    try:
        file_obj.save(path)
    except IOError:
        print('I/O Error')
    file_obj.close()
    file_task = read_csv_task.apply_async(args=[path])

    return make_response(jsonify({'task_id': file_task.task_id}))


@celery.task(bind=True)
def read_csv_task(self, path):
    self.update_state(state=states.PENDING)
    df = pd.read_csv(path, encoding='utf-8', delimiter=",", quoting=csv.QUOTE_NONE)
    result = {}
    for result in insert_data(df):
        report_every_registers = ceil(int(result.get("total"))/2000)
        if result.get("current") % report_every_registers == 0:
            self.update_state(state='PROCESSING', meta=result)
    return result


@products.route('/task/<task_id>', methods=['GET'])
def check_task_status(task_id):
    task = read_csv_task.AsyncResult(task_id)
    if task.state == 'PROCESSING':
        response = {
            'state': task.state,
            'current': task.info.get('current', 0),
            'total': task.info.get('total', 1),
            'status': '%s%%' % int((int(task.info.get('current', 0))*100)/int(task.info.get('total', 1)))
        }
    elif task.state != 'FAILURE':
        response = {
            'state': task.state,
            'current': task.info.get('current', 0),
            'total': task.info.get('total', 1),
            'status': '%s%%' % int((int(task.info.get('current', 0))*100)/int(task.info.get('total', 1)))
        }
        if 'result' in task.info:
            response['result'] = task.info['result']
    else:
        # something went wrong in the background job
        response = {
            'state': task.state,
            'current': 0,
            'total': 0,
            'status': str(task.info),  # this is the exception raised
        }
    return jsonify(response)
