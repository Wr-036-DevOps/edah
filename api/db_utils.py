from api.utils import read_xlsx
import mysql.connector
import xlwt
import requests
import json
from datetime import datetime
# import pandas.io.sql as sql
from api import DatabaseConfig as db_conf


class DbConnectionError(Exception):
    pass


# function to connect to the mysql database
def __connect_to_db(db_name):
    connect = mysql.connector.connect(
        host=db_conf.host,
        user=db_conf.user,
        password=db_conf.password,
        auth_plugin='mysql_native_password',
        database=db_name
    )
    return connect


def health_db():
    db = __connect_to_db("billdb")
    cur = db.cursor(buffered=True)
    cur.execute("SELECT 1")
    db.commit()
    cur.close()


def insert_new_record():
    testsdb = __connect_to_db('billdb')
    cur = testsdb.cursor()
    insert_command = "INSERT INTO Provider (`name`) VALUES ('ALL'), ('pro1'),('pro2')"
    cur.execute(insert_command)

    testsdb.commit() # Don't forget to commit
    return "Record added sucessfully"


def edith_record_in_provider(id, name):
    testsdb = __connect_to_db('billdb')
    cur = testsdb.cursor()
    sql = "UPDATE Provider SET name = %s WHERE id = %s"
    val = (name, id)
    cur.execute(sql, val)
    testsdb.commit()
    return "Record update sucessfully"


def get_record_in_provider(id):
    testsdb = __connect_to_db('billdb')
    cur = testsdb.cursor()
    cur.execute(f"SELECT * FROM Provider WHERE id={id}")
    data = cur.fetchall()

    return data


def get_data_in_rates(product_id):
    testsdb = __connect_to_db('billdb')
    cur = testsdb.cursor()
    cur.execute("SELECT * FROM Rates WHERE product_id = %s", (product_id,))
    data = cur.fetchall()

    return data


def get_all_record():
    testsdb = __connect_to_db('billdb')
    cur = testsdb.cursor()
    cur.execute(f"SELECT * FROM Provider")
    data = cur.fetchall()

    return data


def add_new_reckord_in_truck(id, provider_id):
    testsdb = __connect_to_db('billdb')
    cur = testsdb.cursor()
    sql = "INSERT INTO Trucks (id, provider_id) VALUES (%s, %s)"
    val = (id, provider_id)
    cur.execute(sql, val)
    testsdb.commit()
    return "Record added sucessfully"


def add_new_record_in_rate(product, rate, scope):
    testsdb = __connect_to_db('billdb')
    cur = testsdb.cursor()

    if not get_data_in_rates(product):
        sql = "INSERT INTO Rates (`product_id`, `rate`, `scope`) VALUES (%s, %s, %s)"
        val = (product, rate, scope)
    else:
        sql = "UPDATE Rates SET rate = %s, scope = %s WHERE product_id = %s"
        val = (rate, scope, product)

    print("executing sql query %s", sql)
    cur.execute(sql, val)
    testsdb.commit()
    return "Record update sucessfully"


def edith_record_in_truck(id, provider_id):
    testsdb = __connect_to_db('billdb')
    cur = testsdb.cursor()
    sql = "UPDATE Trucks SET provider_id = %s WHERE id = %s"
    val = (provider_id, id)
    cur.execute(sql, val)
    testsdb.commit()
    return "Record update sucessfully"


def save_to_db_from_file(filename: str):
    key = filename.rsplit('.', maxsplit=1)[0]
    data_from_file = read_xlsx(filename, start_row=1)[key]

    for data in data_from_file:
        product, rate, scope = data
        print(product, rate, scope)
        add_new_record_in_rate(product, rate, scope)

        return "File %s sucessfully processed into the db" %filename


def get_all_record_in_rates():
    testsdb = __connect_to_db('billdb')
    cur = testsdb.cursor()
    cur.execute(f"SELECT * FROM Rates")
    data = cur.fetchall()

    return data

def get_all_trucks_of_provider(id):
    testsdb = __connect_to_db('billdb')
    cur = testsdb.cursor()
    cur.execute("SELECT * FROM Trucks WHERE provider_id = %s", (id,))
    data = cur.fetchall()
    return data

def get_truck_data(id, t1, t2):
    req = requests.get('localhost:8084/item/' + str(id) + '?from=' + str(t1) + '&to=' +str(t2))
    data = json.loads(req.content)
    return data

def get_session_data(id):
    req = requests.get('localhost:8084/session/' + str(id))
    data = json.loads(req.content)
    return data

def get_data_from_weight(t1, t2):
    req = requests.get('localhost:8084/weight?frm='+ str(t1) +'&to='+ str(t2) +'&filter=\'out\'')
    data = json.loads(req.content)
    return data

def create_bill():
    bill = {}

    bill['id'] = ''
    bill['name'] = ''
    bill['from'] = ''
    bill['to'] = ''
    bill['trucksCount'] = 0
    bill['sessionscount'] = 0
    bill['products'] = []
    bill['total'] = 0

    return bill

def create_products():
    products = {}

    products['product'] = ''
    products['count'] = 0
    products['amount'] = 0
    products['rates'] = 0
    products['pay'] = 0

    return products