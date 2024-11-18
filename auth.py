from flask import request, jsonify
from dotenv import load_dotenv
import os

load_dotenv()

def validate_api_key():
    api_key = request.headers.get('x-api-key')
    print('ping')
    if api_key != os.getenv("API_KEY"):
        response = jsonify({"error": "Invalid API key"})
        response.status_code = 401
        return response