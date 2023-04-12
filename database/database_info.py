from pymongo import MongoClient
import os
from dotenv import load_dotenv

#  load environment variables from .env file
load_dotenv()

# # # get environment variables
MONGODB_URI= os.environ.get('MONGODB_URL')
print(MONGODB_URI)
DB_NAME = os.environ.get('DATABASE_NAME')
Customers = os.environ.get('COLLECTION_NAME_Customers')
Pizza = os.environ.get('COLLECTION_NAME_pizza')



client = MongoClient(MONGODB_URI)
db = client[DB_NAME]
customers = db.Customers
pizza = db.Pizza



    

