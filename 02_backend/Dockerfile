FROM python:3.7

WORKDIR /app

COPY 02_backend/API-Gateway/requirements.txt .
COPY 02_backend/API-Gateway/api.py .


COPY 02_backend/lambda-get-data/lambda_function.py lambda_get_data.py
COPY 02_backend/lambda-process-file/lambda_function.py lambda_process_file.py
COPY 02_backend/lambda-send-mail/lambda_function.py lambda_send_mail.py
COPY 02_backend/lambda-send-mail/Stori-horizontal-11.jpg .
COPY 02_backend/common/util.py .


RUN pip install --no-cache-dir -r requirements.txt

# SET env variables
ENV DB_USERNAME=xxxx
ENV DB_PASSWD=xxxx
ENV DB_URL=xxxx
ENV DB_DBNAME=xxxx
ENV environment=local

ENV EMAIL_SMTP_SERVER=smtp-mail.outlook.com
ENV EMAIL_SENDER=email@outlook.com
ENV EMAIL_USER=email@outlook.com
ENV EMAIL_PASS=12345

EXPOSE 5000

CMD ["python", "api.py"]
