from bson import ObjectId
from flask import jsonify, request, Blueprint
from flask_cors import CORS
from db import users
from hash import sha256_hash
from dotenv import load_dotenv
import os

load_dotenv()

user_routes = Blueprint('user_routes', __name__)
CORS(user_routes)

@user_routes.route('/data/<uid>', methods=['GET', 'OPTIONS'])
def get_data(uid):
    print('ping')
    user = users.find_one({'_id': ObjectId(uid)})
    if user:
        user['_id'] = str(user['_id'])
        del user['password']
        return jsonify(user)
    return jsonify({'status': 'user does not exist'})

@user_routes.route('/addUser', methods=['POST'])
def add_user():
    body = request.json
    body['username'] = body['username'].lower()
    if users.find_one({'username': body['username'].lower()}):
        return jsonify({'status': 'Someone with that username already exists!'})
    body['accounts'] = [{
        'account_name': 'Unallocated funds',
        'weight': 1.0,
        'balance': 0
    }]
    body['transactions'] = []
    body['income'] = []
    body['balance'] = 0.0
    body['password'] = sha256_hash(body['password'])
    id = users.insert_one(body).inserted_id
    user = users.find_one({'_id':id})
    user['_id'] = str(user['_id'])
    del user['password']
    return {
        'user': user,
        'apiKey': os.getenv('API_KEY')
    }


@user_routes.route('/authenticate', methods=['POST'])
def auth():
    msg = ''
    result = {}
    data = request.json
    username = data['username']
    password = sha256_hash(data['password'])
    user = users.find_one({'username':username.lower()})
    if user:
        if password == user['password']:
            user['_id'] = str(user['_id'])
            del user['password']
            msg = 'successfully logged in'
            result['user'] = user
            result['apiKey'] = os.getenv('API_KEY')
        else:
            msg = 'invalid password'
    else:
        msg = 'please enter a valid username'
    result['status'] = msg
    return result

@user_routes.route('/deleteUser/<uid>', methods=['DELETE'])
def del_user(uid):
    id = ObjectId(uid)
    if users.find_one({'_id': id}):
        users.delete_one({'_id': id})
        return jsonify({'status': 'success'})
    return jsonify({'status': 'user does not exist'})