import os
from io import StringIO 
import csv
from flask import Flask, jsonify, request
from flask_cors import CORS
from lambda_process_file import lambda_handler as lambda_process_file_handler
from lambda_send_mail import lambda_handler as lambda_send_mail_handler
from lambda_get_data import lambda_handler as lambda_get_data_handler

app = Flask(__name__)
CORS(app)

@app.route('/process-file', methods=['POST'])
def process_file():
    print('-API-Gateway - process_file-')
    
    file_attached = request.files['file']    
    str_file = file_attached.read().decode('ascii')
    
    json_payload = {"body":{
                            "filename": file_attached.filename,
                            "filecontent":StringIO(str_file)
                            }
                    }
    
    return jsonify(lambda_process_file_handler(json_payload, "dummy"))

@app.route('/get-data', methods=['GET'])
def get_data():
    print('-API-Gateway - get_data-')
    temp = lambda_get_data_handler("dummy1","dummy2")
    return temp['body']

@app.route('/send-mail', methods=['POST'])
def send_mail():
    print('-API-Gateway - send_mail-')
    json_payload = {"body":{
                            "client_id": request.json['client_id'],
                            }
                    }

    temp = lambda_send_mail_handler(json_payload,"dummy2")

    return jsonify(temp)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
