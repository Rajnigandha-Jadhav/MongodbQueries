from flask import Flask, request, jsonify
from database.database_info import customers, pizza
from validations.validation import CustomerSchema, PizzaSchema
from bson import ObjectId
from dataclasses import asdict
import json
customer_schema = CustomerSchema()
pizza_schema = PizzaSchema()

app = Flask(__name__)

# Create a pizza document


@app.route('/pizza', methods=['POST'])
def create_pizza():
    try:
        pizza_data = request.json
        if not pizza_data:
            return "Please provide the data", 400
        # Create a Pizza object using the loaded pizza data attributes
        pizzaInfo = pizza_schema.load(pizza_data)
        print(pizza)
        pizza.insert_one(asdict(pizzaInfo))
        resp = jsonify({'message': 'Pizza information saved successfully'})
        resp.status_code = 201
        return resp
    except Exception as e:
        return f"An error occurred: {str(e)}", 500


@app.route('/many-pizza', methods=['POST'])
def create_many_pizza():
    try:
        data = request.json
        # Convert the array of objects to a list of JSON data documents
        json_data_list = [json.dumps(d) for d in data]

        # Insert the JSON data into the MongoDB collection

        pizza.insert_many([json.loads(d) for d in json_data_list])

        resp = jsonify({'message': 'Pizza information saved successfully'})
        resp.status_code = 201
        return resp
    except Exception as e:
        return f"An error occurred: {str(e)}", 500


# Get all pizza according to the size...write 1 if you want to fetch all pizza info.
@app.route('/all-pizza', methods=['GET'])
def get_all_pizza():
    try:
        pipeline = [
            {
                '$unwind': {
                    'path': '$toppings'
                }
            },
            {
                '$group': {
                    '_id': '$_id',
                    'pizzaName': {'$first': '$pizzaName'},
                    'size': {'$first': '$size'},
                    'price': {'$first': '$price'},
                    'toppings': {'$push': '$toppings'}
                }
            },
            {
                '$project': {
                    '_id': 0,
                    'pizzaName': 1,
                    'size': 1,
                    'price': 1,
                    'toppings': 1
                }
            }
        ]
        pizzas = pizza.aggregate(pipeline)
        return jsonify(list(pizzas)), 200
    except Exception as e:
        return f"An error occurred: {str(e)}", 500


# Create details of all the customers with the order they have placed and the total price of the order..
@app.route('/customers', methods=['POST'])
def create_customers():
    try:
        customer_data = request.json
        print(customer_data)
        if not customer_data:
            return "Please provide the data", 400
        customerInfo = customer_schema.load(customer_data)

        pizza_price = pizza.find_one({'_id': ObjectId(customerInfo.order)})
        key = pizza_price.get('price')
        cost = int(key)
        obj = asdict(customerInfo)
        obj["totalPrice"] = (customerInfo.orderQuantity)*(cost)

        customers.insert_one(obj)
        resp = jsonify({'message': 'Customer information saved successfully'})
        resp.status_code = 201
        return resp
    except Exception as e:
        return f"An error occurred: {str(e)}", 500


# Fetch details of the all customers with the information of the pizza that they have ordered..
@app.route('/all-customers', methods=['GET'])
def get_customers():
    try:
        cust_info = customers.find()
        cust_list = []
        for customer in cust_info:
            # Find order with size Medium and topping Paneer
            orderDetails = pizza.find_one({
                "_id": ObjectId(customer["order"]),
                "size": "Medium", "toppings.name": "Paneer"}
            )

        # Convert _id to string for JSON serialization
        orderDetails["_id"] = str(orderDetails["_id"])

        cust_dict = {
            'name': customer['name'],
            'location': customer['location'],
            'order': orderDetails,
            'orderQuantity': customer['orderQuantity'],
            'totalPrice': customer['totalPrice']
        }
        cust_list.append(cust_dict)

        resp = jsonify(cust_list)
        resp.status_code = 200
        return resp

    except Exception as e:
        return f"An error occurred: {str(e)}", 500


# Update a document
@app.route('/pizza/<string:pizza_id>', methods=['PUT'])
def update_pizza(pizza_id):
    try:
        pizza.update_one({'_id': ObjectId(pizza_id)}, {
                         '$set': {'size': 'Extra-Large', 'toppings.0.name': 'baby corns'}})
        resp = jsonify({'message': 'Pizza information updated successfully'})
        resp.status_code = 200
        return resp
    except Exception as e:
        return f"An error occurred: {str(e)}", 500


# update many documents
@app.route('/pizzass', methods=['PUT'])
def update_many_pizza():
    try:
        filter_criteria = {'size': 'Large'}
        update_data = {'$set': {'size': 'Extra-Extra-Large',
                                'toppings.0.name': 'baby corns'}}
        result = pizza.update_many(filter_criteria, update_data)

        if result.modified_count > 0:
            resp = jsonify(
                {'message': f'{result.modified_count} pizzas updated successfully'})
            resp.status_code = 200
        else:
            resp = jsonify({'message': 'No pizzas were updated'})
            resp.status_code = 404

        return resp
    except Exception as e:
        return f"An error occurred: {str(e)}", 500


@app.route('/insert-pizza', methods=['PUT'])
def upsert_pizzas():
    try:
        filter_criteria = {'size': 'Extra-Small'}
        update_data = {'$set': {'pizzaName': "Indian Pizza", 'size': 'small',
                                'price': 200, 'toppings.0': {"name": 'Capsicum', "quantity": 4}}}
        result = pizza.update_many(filter_criteria, update_data, upsert=True)

        if result.modified_count > 0 or result.upserted_id is not None:
            count = result.modified_count + \
                (1 if result.upserted_id is not None else 0)
            resp = jsonify({'message': f'{count} pizzas updated successfully'})
            resp.status_code = 200
        else:
            resp = jsonify({'message': 'No pizzas were updated or inserted'})
            resp.status_code = 404

        return resp
    except Exception as e:
        return f"An error occurred: {str(e)}", 500






# @app.route('/bulk-ops', methods=['POST'])
# def bulk_op():
#     try:

#         bulk_ops = [
#             {
#                 "updateOne": {
#                     {"pizzaName": "Indian Pizza"},
#                     {"$set": {"price": 400}}
#                 }
#             },
#             {
#                 "insertOne": {
#                     {"pizzaName": "American Pizza", "size": "Medium", "price": 500}
#                 }
#             },
#             {
#                 "deleteOne": {
#                     {"pizzaName": "Cheese Pizza"}
#                 }
#             }
#         ]

#         result = pizza.bulk_write(bulk_ops)
#         resp = jsonify({'message': ' pizzas were updated or inserted or deleted','data':result.bulk_api_result})
#         resp.status_code = 404

#         return resp

#     except Exception as e:
#         return f"An error occurred: {str(e)}", 500


@app.route('/customers/<string:customer_id>', methods=['DELETE'])
def delete_customer(customer_id):
    try:
        result = customers.delete_one({'_id': ObjectId(customer_id)})
        if result.deleted_count == 0:
            return "Customer not found", 404
        else:
            return "Customer deleted successfully", 204
    except Exception as e:
        return f"An error occurred: {str(e)}", 500


if __name__ == '__main__':
    app.run(debug=True)
