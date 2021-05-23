from flask import Flask, jsonify

import config
from config import database_string
from database import init_engine, init_db
from auth.auth import auth
from products.products import products
from docs.swagger import swagger_ui_blueprint, SWAGGER_URL
from api_specs import spec

from flask_jwt_extended import JWTManager

app = Flask(__name__)

# Database configuration and initialization
app.config['SQLALCHEMY_DATABASE_URI'] = database_string
init_engine(app.config['SQLALCHEMY_DATABASE_URI'])
init_db()

# Setup the Flask-JWT-Extended extension
app.config["JWT_SECRET_KEY"] = config.cfg.get("auth").get("jwt_key")
jwt = JWTManager(app)

# register blueprints. Easy to build versioned APIs
app.register_blueprint(auth, url_prefix="/api/v1/auth")
app.register_blueprint(products, url_prefix="/api/v1/products")
app.register_blueprint(swagger_ui_blueprint, url_prefix=SWAGGER_URL)

# register all swagger documented functions
with app.test_request_context():
    for fn_name in app.view_functions:
        if fn_name == 'static':
            continue
        view_fn = app.view_functions[fn_name]
        spec.path(view=view_fn)


# swagger json endpoint
@app.route("/api/swagger.json")
def create_swagger_spec():
    """
        Swagger API definition.
    """
    return jsonify(spec.to_dict())


if __name__ == "__main__":
    app.run(host='0.0.0.0')
