import json
import io
import os
import psycopg2
from datetime import datetime

def insert_data(file, filename):
    print('--insert_data--')
    try:
        connection = psycopg2.connect(user=os.environ['DB_USERNAME']
                                    , password=os.environ['DB_PASSWD']
                                    , host=os.environ['DB_URL']
                                    , port="5432"
                                    , database=os.environ['DB_DBNAME'])
        
        # print('--connected--')

        # Get the current date and time
        now = datetime.now()
        formatted_date = now.strftime("%Y-%m-%d %H:%M:%S")

        with connection.cursor() as cursor:

            lines = file.split("\n")

            # We're assuming first line in the file is header
            for line in lines[1:]:
                elements = line.split(",")

                # This is because last line in the file could be empty:
                if len(elements) > 1:
                    # print()
                    # print(elements)
                    cursor.execute("INSERT INTO transaction (client_id, txn_date, amount, batch_file) VALUES (%s, %s, %s, %s)", (elements[0], elements[1], elements[2], formatted_date+"_"+filename))

            connection.commit()

        connection.close()

    except Exception as error:
        print('ERROR')
        print(error)
    
def get_file_info(event):

    if os.environ['environment'] == 'local':
        print('--Runs locally')
        filename = event['body']['filename']
        file = event['body']['filecontent'].read()
    
    if os.environ['environment'] == 'AWS':
        print('--Runs AWS')
        io_elements = io.StringIO(event['body']).read()
        elements = io_elements.split('\r\n')
        filename = elements[1].split(";")[2][11:-1]
        
        file = elements[4]

    return file, filename

def lambda_handler(event, context):
    print('-lambda-process-function.lambda_handler-')

    file, filename = get_file_info(event)
    insert_data(file, filename)

    return {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
        },
        'body': json.dumps('Hello from Lambda!')
    }
