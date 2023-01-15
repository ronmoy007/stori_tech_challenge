import json
import io
import os
import mimetypes
import psycopg2
import smtplib

from email.message import EmailMessage
from email.utils import make_msgid

from util import read_data

def send_email(client_id):
    print('--send_email--')
    summary_data, months_data = read_data(client_id)

    user_name = summary_data[0][1]
    user_mail = summary_data[0][2]
    user_average_credit = summary_data[0][3]
    user_average_debit = summary_data[0][4]
    user_total_balance = summary_data[0][5]

    sender = os.environ['EMAIL_SENDER']
    recipient = os.environ['EMAIL_SENDER']
    
    email = EmailMessage()
    email["Subject"] = "Stori challenge email"
    email["From"] = sender
    email["To"] = recipient
    email["CC"] = user_mail

    string_txns_by_month_plain = ""
    string_txns_by_month_html = ""
    for line in months_data:
        string_txns_by_month_plain = string_txns_by_month_plain + f"Number of transactions in {line[3]} {line[4]}:\r\n\r\n"
        string_txns_by_month_html = string_txns_by_month_html + f"<tr><td align='right'>{line[2]}</td><td align='right'>{line[4]}</td><td align='right'>{line[5]}</td></tr>"

    plain_text = f"Summary of transactions for {user_name}\r\n"
    f"Total balance is {user_total_balance:.2f}\r\n\r\n"
    f"{string_txns_by_month_plain}"
    f"Average credit amount: {user_average_credit:.2f}:\r\n\r\n"        
    f"Average debit amount: {user_average_debit:.2f}:\r\n\r\n"
    f"Greetings\r\n"
    
    email.set_content(plain_text)
    image_cid = make_msgid(domain="xyz.com")
    email.add_alternative(
            f"""\
        <html>
        <head>
        <style>
        table, th, td {{
        border: 1px solid black;
        border-collapse: collapse;
        }}
        </style>
        </head>
        <body>
            <img src="cid:{image_cid[1:-1]}">
            <table style="width:100%">
                <caption><strong>Summary for {user_name}</strong></caption>
                <thead>
                    <tr>
                        <th><span style="font-weight: 400; text-align: start; background-color: rgb(255, 255, 255);">Total balance</span><br></th>
                        <th><span style="font-weight: 400; text-align: start; background-color: rgb(255, 255, 255);">Average credit amount</span><br></th>
                        <th><span style="font-weight: 400; text-align: start; background-color: rgb(255, 255, 255);">Average debit amount</span></th>
                    </tr>
                </thead>	
                <tbody>	
                    <tr>
                        <td align='right'>${user_total_balance:.2f}</td>
                        <td align='right'>${user_average_credit:.2f}</td>
                        <td align='right'>${user_average_debit:.2f}</td>
                    </tr>
                </tbody>
            </table>
            <br><br>
            <table style="width:100%">
                <caption><strong>Transactions per month for {user_name}</strong></caption>
                <thead>
                    <tr>
                        <th><span style="font-weight: 400; text-align: left; background-color: rgb(255, 255, 255);">Year</span><br></th>
                        <th><span style="font-weight: 400; text-align: left; background-color: rgb(255, 255, 255);">Month</span><br></th>
                        <th><span style="font-weight: 400; text-align: left; background-color: rgb(255, 255, 255);">Number of transactions</span></th>
                    </tr>
                </thead>
                <tbody>	
                    {string_txns_by_month_html}
                </tbody>
            </table>
        </body>
        </html>
        """, subtype="html",
        )

    img_logo = "Stori-horizontal-11.jpg" 
    with open(img_logo, "rb") as img:
        maintype, subtype = mimetypes.guess_type(img.name)[0].split("/")
        email.get_payload()[1].add_related(img.read(), maintype=maintype, subtype=subtype, cid=image_cid)

    smtp = smtplib.SMTP(os.environ['EMAIL_SMTP_SERVER'], port=587)
    smtp.starttls()
    smtp.login(os.environ['EMAIL_USER'], os.environ['EMAIL_PASS'])
    smtp.sendmail(os.environ['EMAIL_SENDER'], recipient, email.as_string())
    smtp.quit()
    
def get_client(event):

    if os.environ['environment'] == 'local':
        print('--Runs locally')
        client_id = event['body']['client_id']
    
    if os.environ['environment'] == 'AWS':
        print('--Runs AWS')
        io_elements = io.StringIO(event['body']).read()
        client_id = json.loads(io_elements)['client_id']

    return client_id

def lambda_handler(event, context):
    print('-lambda-send-mail.lambda_handler-')
    
    client_id = get_client(event)
    send_email(client_id)

    return {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
        },
        'body': "Dummy body"
    }
