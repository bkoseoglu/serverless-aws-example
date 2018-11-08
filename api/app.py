# app.py

import os

import boto3

from flask import Flask, jsonify, request
app = Flask(__name__)

USERS_TABLE = os.environ['USERS_TABLE']
IS_OFFLINE = os.environ.get('IS_OFFLINE')

if IS_OFFLINE:
    client = boto3.client(
        'dynamodb',
        region_name='localhost',
        endpoint_url='http://localhost:8000'
    )
else:
    client = boto3.client('dynamodb')
client = boto3.client('dynamodb')

@app.route("/")
def hello():
    return jsonify(dict(os.environ))


@app.route("/users/<string:user_id>")
def get_user(user_id):
    if request.is_json:
        resp = client.get_item(
            TableName=USERS_TABLE,
            Key={
                'userId': { 'S': user_id }
            }
        )
        item = resp.get('Item')
        if not item:
            return jsonify({'error': 'User does not exist'}), 404

        return jsonify({
            'userId': item.get('userId').get('S'),
            'name': item.get('name').get('S')
        })
    else:
        return jsonify({'error': 'Bad request, json request is expected'}), 400


@app.route("/users", methods=["POST"])
def create_user():
    if request.is_json:
        user_id = request.json.get('userId')
        name = request.json.get('name')
        if not user_id or not name:
            return jsonify({'error': 'Please provider userId and name'}), 400

        resp = client.put_item(
            TableName=USERS_TABLE,
            Item={
                'userId': {'S': user_id },
                'name': {'S': name }
            }
        )
    else:
        return jsonify({'error': 'Bad request, json request is expected'}), 400

    return jsonify({
        'userId': user_id,
        'name': name
    })