from flask_lambda import FlaskLambda
import json
import boto3
from boto3.dynamodb.conditions import Key
from flask import Flask, jsonify, request,render_template,redirect
import pandas as pd
client = boto3.resource('dynamodb', region_name='ap-south-1')
dynamoTableName=client.Table('customerstable')
app = FlaskLambda(__name__)

@app.route('/hello')
def index():
    data = {"message":'Hello world 22'}
    return json.dumps(data), 200, {'Content-Type':'application/json'}

@app.route('/home', methods=["GET"])
def home():
    return render_template('/search.html')

@app.route('/search', methods=["POST"])
def search():
    res,res2=[],[]
    search_string=request.form.get('search')
    res=dynamoTableName.query(IndexName='First_Name-index',KeyConditionExpression=Key('First Name').eq(search_string))
    res2=dynamoTableName.query(IndexName='Last_Name-index',KeyConditionExpression=Key('Last Name').eq(search_string))
    result=res['Items']+res2['Items']
    if result:
        # return json.dumps(pd.DataFrame(result).astype(str).to_dict('records'),indent=2)
        return render_template('/search.html',data=json.dumps(pd.DataFrame(result).astype(str).to_dict('records'),indent=2))
    else:
        return json.dumps({'Message':'No match found'})
