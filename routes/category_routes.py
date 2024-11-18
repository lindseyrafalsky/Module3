from flask import jsonify, request, Blueprint
from flask_cors import CORS
from db import users
from bson import ObjectId

category_routes = Blueprint('category_routes', __name__)
CORS(category_routes)

@category_routes.route('/addCategory/<uid>', methods=['POST'])
def add_category(uid):
    id = ObjectId(uid)
    user = users.find_one({'_id': id})
    unallocated = user['accounts'][0]['weight']

    body = request.json
    account_weight = body['weight']
    unallocated -= account_weight
    

    body['balance'] = user['balance'] * account_weight
    unallocated_balance = user['accounts'][0]['balance'] - body['balance']
    update_operations = {
        '$push': {'accounts': body},
    }
    users.update_one(user, update_operations)
    users.update_one({'_id': id}, {'$set': {'accounts.0.weight': unallocated, 'accounts.0.balance': unallocated_balance}})
    user = users.find_one({'_id':id})
    user['_id'] = str(user['_id'])
    del user['password']
    return jsonify({'status': 'added', 'user': user})

@category_routes.route('/deleteCategory/<uid>', methods=['DELETE'])
def del_category(uid):
    id = ObjectId(uid)
    user = users.find_one({'_id': id})
    unallocated_bal = user['accounts'][0]['balance']
    unallocated_weight = user['accounts'][0]['weight']
    category = request.args.get('category')
    for i in range(len(user['accounts'])):
        account = user['accounts'][i]
        if account['account_name'] == category:
            balance = account['balance']
            weight = account['weight']
            users.update_one({'_id': id}, {'$set': {'accounts.0.balance': unallocated_bal + balance, 'accounts.0.weight': unallocated_weight + weight}})
            users.update_one({'_id': id}, {'$pull': {'accounts': {'account_name': category}}})
            user = users.find_one({'_id':id})
            user['_id'] = str(user['_id'])
            del user['password']
            return jsonify({'status':'success', 'user': user})
    return jsonify({'status':'account does not exist'})

@category_routes.route('/moveFunds/<uid>', methods=['POST'])
def move_funds(uid):
    id = ObjectId(uid)
    user = users.find_one({'_id': id})

    body = request.json
    transfer_from = body['from']
    transfer_to = body['to']
    amount = body['amount']
    from_index = 0
    from_balance = 0
    to_index = 0
    to_balance = 0

    for i in range(len(user['accounts'])):
        if user['accounts'][i]['account_name'] == transfer_from:
            from_index = i
            from_balance = user['accounts'][i]['balance']
        elif user['accounts'][i]['account_name'] == transfer_to:
            to_index = i
            to_balance = user['accounts'][i]['balance']

    users.update_one({'_id':id}, {'$set': {f'accounts.{from_index}.balance': from_balance - amount, f'accounts.{to_index}.balance':  to_balance + amount}})
    user = users.find_one({'_id':id})
    user['_id'] = str(user['_id'])
    del user['password']
    return jsonify({'status':'success', 'user': user})
