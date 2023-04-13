from flask import Flask,request,jsonify
from database.database_info import queries
app1 = Flask(__name__)

@app1.route('/add-query')
def insert_one():
    info = request.json
    queries.insertOne(info)
    resp = jsonify({'message': 'Pizza information saved successfully'})
    resp.status_code = 201
    return resp





if __name__ == '__main__':
    app1.run(debug=True)
