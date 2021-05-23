from marshmallow import Schema, fields


# Generic schemas
class ActionOutputSchema(Schema):
    result = fields.String(description="Transaction status. success, error, failed", required=True)


#
# Products Schema
#
class CreateProductSchema(Schema):
    name = fields.String(description="Product name", required=True)
    sku = fields.String(description="Product name", required=True)
    description = fields.String(description="Product name", required=True)


# Inheriting CreateMovieSchema elements only adding ID
class ProductSchema(CreateProductSchema):
    id = fields.String(description="Product ID", required=False)


#
# User schema
#
class LoginSchema(Schema):
    password = fields.String(description="Password", required=True)
    user = fields.String(description="Username", required=True)


class LoggedUserSchema(Schema):
    id = fields.Int(description="User ID", required=True)
    jtw = fields.String(description="JWT token", required=True)
