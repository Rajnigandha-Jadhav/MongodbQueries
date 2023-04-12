from marshmallow import Schema, fields, post_load, validate
from model.model import Customer,Pizza


class CustomerSchema(Schema):
    name = fields.Str(required=True)
    location= fields.Str(required=True)
    order= fields.Str(required=True)
    orderQuantity= fields.Int(missing=1)
    

    @post_load
    def make_customer(self, data, **kwargs):
        return Customer(**data)


class PizzaSchema(Schema):
    pizzaName = fields.Str(required=True)
    size = fields.Str(required=True, validate=validate.OneOf(['Small', 'Medium', 'Large']))
    price = fields.Int(required=True)

    @post_load
    def make_pizza(self, data, **kwargs):
        return Pizza(**data)