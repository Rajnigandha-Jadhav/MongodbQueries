from flask import Flask, request, jsonify
from database.database_info import customers,pizza
from validations.validation import CustomerSchema,PizzaSchema
from bson import ObjectId
from dataclasses import asdict
customer_schema = CustomerSchema()
pizza_schema = PizzaSchema()

app = Flask(__name__)

#Create a pizza document
@app.route('/pizza', methods=['POST'])
def create_pizza():
    try:
        pizza_data = request.json
        if not pizza_data:
            return "Please provide the data", 400
        pizzaInfo = pizza_schema.load(pizza_data)  # Create a Pizza object using the loaded pizza data attributes
        print(pizza)
        pizza.insert_one(asdict(pizzaInfo))
        resp = jsonify({'message': 'Pizza information saved successfully'})
        resp.status_code = 201
        return resp
    except Exception as e:
        return f"An error occurred: {str(e)}", 500






#Get all pizza according to the size...write 1 if you want to fetch all pizza info.
@app.route('/all-pizza', methods=['GET'])
def get_all_pizza():
    try:
        pipeline = [
            {
                '$project': {
                    '_id': 0,
                    'pizzaName': 1,
                    'size': "Large",
                    'price': 1,
        
                }
            }
        ]
        pizzas = pizza.aggregate(pipeline)
        return jsonify(list(pizzas)), 200
    except Exception as e:
        return f"An error occurred: {str(e)}", 500




#Create details of all the customers with the order they have placed and the total price of the order..
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
    



#Fetch details of the all customers with the information of the pizza that they have ordered..
@app.route('/all-customers', methods=['GET'])
def get_customers():
    try:
        

        cust_info = customers.find()
        cust_list = []

        for customer in cust_info:
            orderDetails = pizza.find_one({"_id":ObjectId(customer["order"])})
            orderDetails["_id"] = str(orderDetails["_id"])
        
            cust_dict = {}
            cust_dict['name'] = customer['name']
            cust_dict['location'] = customer['location']
            cust_dict['order'] = orderDetails
            cust_dict['orderQuantity'] = customer['orderQuantity']
            cust_dict['totalPrice'] = customer['totalPrice']

            cust_list.append(cust_dict)
        resp = jsonify(cust_list)
        resp.status_code = 200
        return resp
    except Exception as e:
        return f"An error occurred: {str(e)}", 500
    



if __name__ == '__main__':
    app.run(debug=True)
