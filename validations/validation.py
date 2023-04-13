from marshmallow import Schema, fields, post_load, validate
from model.model import Customer,Pizza,Topping


class CustomerSchema(Schema):
    name = fields.Str(required=True)
    location= fields.Str(required=True)
    order= fields.Str(required=True)
    orderQuantity= fields.Int(missing=1)
    

    @post_load
    def make_customer(self, data, **kwargs):
        return Customer(**data)





class ToppingSchema(Schema):
    name = fields.Str()
    quantity = fields.Int()

    @post_load
    def make_topping(self, data, **kwargs):
        return Topping(**data)



class PizzaSchema(Schema):
    pizzaName = fields.Str(required=True)
    size = fields.Str(required=True, validate=validate.OneOf(['Small', 'Medium', 'Large']))
    price = fields.Int(required=True)
    toppings = fields.List(fields.Nested(ToppingSchema))

    @post_load
    def make_pizza(self, data, **kwargs):
        return Pizza(**data)