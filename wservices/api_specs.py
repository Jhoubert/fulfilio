from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from apispec_webframeworks.flask import FlaskPlugin
from schemas import ActionOutputSchema, LoginSchema, LoggedUserSchema, ProductSchema, CreateProductSchema, \
    UpdateProductSchema

spec = APISpec(
    title="",
    version="1.0.0",
    openapi_version="3.0.2",
    plugins=[FlaskPlugin(), MarshmallowPlugin()],
)

# Default schemes
spec.components.schema("ActionOutputSchema", schema=ActionOutputSchema)

# Auth schemes
spec.components.schema("LoginSchema", schema=LoginSchema)
spec.components.schema("LoggedUserSchema", schema=LoggedUserSchema)

# Products schemes
spec.components.schema("ProductSchema", schema=ProductSchema)
spec.components.schema("UpdateProductSchema", schema=UpdateProductSchema)
spec.components.schema("CreateProductSchema", schema=CreateProductSchema)


tags = [
            {'name': 'Users',
             'description': 'User related endpoints'
            },
            {'name': 'Products',
             'description': 'All products related endpoints.'
            }
       ]

for tag in tags:
    spec.tag(tag)
