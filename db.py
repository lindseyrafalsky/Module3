# db.py
from pymongo.mongo_client import MongoClient
import certifi
from dotenv import load_dotenv
import os

load_dotenv()

uri = os.getenv('MONGO_URI')
client = MongoClient(uri, tlsCAFile=certifi.where())
db = client['finance-app']
users = db.user
