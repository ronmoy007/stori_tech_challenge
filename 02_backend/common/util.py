import os
import psycopg2

str_query_months = '''
with credit as (
	SELECT 
		transaction.client_id,
		extract(year from transaction.txn_date) as txn_year_num,
		extract(month from transaction.txn_date) as txn_month_num,
		to_char(transaction.txn_date, 'Month') txn_month_name,
		sum(transaction.amount) as total,
		avg(transaction.amount) average
	FROM transaction
	where amount > 0
	group by 
		transaction.client_id,
		extract(year from transaction.txn_date),
		extract(month from transaction.txn_date),
		to_char(transaction.txn_date, 'Month')
), 
debit as (
	SELECT 
		transaction.client_id,
		extract(year from transaction.txn_date) as txn_year_num,
		extract(month from transaction.txn_date) as txn_month_num,
		to_char(transaction.txn_date, 'Month') txn_month_name,
		sum(transaction.amount) as total,
		avg(transaction.amount) average
	FROM transaction
	where amount < 0
	group by 
		transaction.client_id,
		extract(year from transaction.txn_date),
		extract(month from transaction.txn_date),
		to_char(transaction.txn_date, 'Month')
)
select 
	client.id,
	client.name,
	extract(year from transaction.txn_date) as txn_year_num,
	extract(month from transaction.txn_date) as txn_month_num,
	to_char(transaction.txn_date, 'Month') txn_month_name,
	count(extract(month from transaction.txn_date)) as txn_month_count,
	coalesce(credit.total,0) + coalesce(debit.total,0) as total_balance_by_month,
	coalesce(credit.total,0) as credit_total_by_month,
	coalesce(credit.average,0) as credit_average_by_month,
	coalesce(debit.total,0) as debit_total_by_month,
	coalesce(debit.average,0) as debit_average_by_month
from client
left join transaction on client.id = transaction.client_id
left join credit 
	on (client.id = credit.client_id 
		and extract(year from transaction.txn_date) = credit.txn_year_num
		and extract(month from transaction.txn_date) = credit.txn_month_num)
left join debit 
	on (client.id = debit.client_id 
		and extract(year from transaction.txn_date) = debit.txn_year_num
		and extract(month from transaction.txn_date) = debit.txn_month_num)
{condition}
group by 
	client.id,
	client.name,
	extract(year from transaction.txn_date),
	extract(month from transaction.txn_date),
	to_char(transaction.txn_date, 'Month'),
	credit.total,
	credit.average,
	debit.total,
	debit.average
order by 
	client.id,
	extract(year from transaction.txn_date),
	extract(month from transaction.txn_date)
'''

str_query_summary = '''
with credit as (
	SELECT 
		transaction.client_id,
		sum(transaction.amount) as total,
		avg(transaction.amount) average
	FROM transaction
	where amount > 0
	group by transaction.client_id
),
debit as (
	SELECT 
		transaction.client_id,
		sum(transaction.amount) as total,
		avg(transaction.amount) average
	FROM transaction
	where amount < 0
	group by transaction.client_id
)
select 
	client.id,
	client.name,
	client.email,
	credit.average as credit_average,
	debit.average as debit_average,
	credit.total+debit.total as total_balance
from client
left join credit on client.id = credit.client_id
left join debit on client.id = debit.client_id
{condition}
order by 1
'''

def read_data(client_id = None):
    
    print('--read_data--')
    if client_id is None:
        condition = ""
    else:
        condition = f"where client.id = {client_id}"

    try:
        connection = psycopg2.connect(user=os.environ['DB_USERNAME']
                                    , password=os.environ['DB_PASSWD']
                                    , host=os.environ['DB_URL']
                                    , port="5432"
                                    , database=os.environ['DB_DBNAME'])

        with connection.cursor() as cursor:
                        
            cursor.execute(str_query_summary.format(condition=condition))
            rows = cursor.fetchall()
            summary_list = []
            for row in rows:
                summary_list.append(row)

            cursor.execute(str_query_months.format(condition=condition))
            rows = cursor.fetchall()
            months_list = []
            for row in rows:
                months_list.append(row)

        connection.close()

        return summary_list, months_list

    except Exception as error:
        print('ERROR')
        print(error)
