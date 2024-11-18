from flask import jsonify, request, Blueprint
from flask_cors import CORS
from db import users
from bson import ObjectId
from datetime import datetime


transaction_routes = Blueprint('transaction_routes', __name__)
CORS(transaction_routes)

@transaction_routes.route('/addTransaction/<uid>', methods=['POST'])
def add_transaction(uid):
    id = ObjectId(uid)
    user = users.find_one({'_id':id})

    current_datetime = datetime.now()
    date_time_stamp = current_datetime.strftime("%Y-%m-%d %H:%M:%S")

    body = request.json
    body['date'] = date_time_stamp

    for i in range(len(user['accounts'])):
        account = user['accounts'][i]
        if body['account_name'] == account['account_name']:
            curr_balance = account['balance']
            users.update_one({'_id':id}, {'$push': {'transactions': body}})
            users.update_one({'_id':id}, {'$set': {f'accounts.{i}.balance': curr_balance - body['amount'], 'balance': user['balance'] - body['amount']}})
            user = users.find_one({'_id':id})
            user['_id'] = str(user['_id'])
            del user['password']
            return jsonify({'status': 'added', 'user': user})
    return jsonify({'status': 'account does not exist'})
