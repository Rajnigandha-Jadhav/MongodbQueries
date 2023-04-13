from dataclasses import dataclass
from typing import List
from dataclass_wizard import JSONSerializable

@dataclass
class Customer(JSONSerializable):
    name: str
    location: str
    order: str
    orderQuantity: int

@dataclass
class Topping:
    name: str
    quantity: int

@dataclass
class Pizza:
    pizzaName: str
    size: List[str]
    price: int
    toppings: List[Topping]

