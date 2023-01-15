import json
import io
import os
import psycopg2
from datetime import datetime
import decimal
from util import read_data

class Encoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, decimal.Decimal): return float(obj)

def lambda_handler(event, context):
    print('-lambda-get-data.lambda_handler-')

    summary_data, months_data = read_data()
    
    payload = {
                'summary_data':summary_data,
                'months_data':months_data
                }

    return {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
        },
        'body': json.dumps(payload, cls = Encoder)
    }
