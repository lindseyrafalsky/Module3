from flask import jsonify, request, Blueprint
from flask_cors import CORS
from db import users
from bson import ObjectId
from datetime import datetime


income_routes = Blueprint('income_routes', __name__)
CORS(income_routes)

@income_routes.route('/addPayday/<uid>', methods=['POST'])
def add_income(uid):
    id = ObjectId(uid)
    user = users.find_one({'_id': id})

    current_datetime = datetime.now()
    date_time_stamp = current_datetime.strftime("%Y-%m-%d %H:%M:%S")

    body = request.json
    body['date'] = date_time_stamp

    total = 0

    for i in range(len(user['accounts'])):
        account = user['accounts'][i]
        balance = account['balance']
        to_add = account['weight'] * body['amount']
        new_balance = balance + to_add
        total += new_balance
        users.update_one({'_id': id}, {'$set': {f'accounts.{i}.balance': new_balance}})

    operations = {
        '$push': {'income': body},
        '$set': {'balance': total}
    }

    users.update_one({'_id': id}, operations)

    user = users.find_one({'_id':id})
    user['_id'] = str(user['_id'])
    del user['password']

    return jsonify({'status': 'added', 'user': user})


@income_routes.route('/addBalance/<uid>', methods=['POST'])
def add_balance(uid):
    id = ObjectId(uid)
    user = users.find_one({'_id': id})

    body = request.json
    category = body['category']
    amount = body['amount']

    current_datetime = datetime.now()
    date_time_stamp = current_datetime.strftime("%Y-%m-%d %H:%M:%S")

    income = {
        'amount': float(amount),
        'date': date_time_stamp,
        'description': body['description']
    }

    for i in range(len(user['accounts'])):
        account = user['accounts'][i]
        if account['account_name'] == category:
            print(user['accounts'][i]['balance'])
            user['accounts'][i]['balance'] += float(amount)
            user['balance'] += float(amount)
            user['income'].append(income)
            users.update_one({'_id': id}, {'$set': user})
            user['_id'] = str(user['_id'])
            del user['password']
            return jsonify({'status': 'added', 'user': user})
    return jsonify({'status': 'account does not exist'})


