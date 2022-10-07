from crypt import methods
from itertools import count, product
from flask import jsonify, request, redirect, url_for
from . import db_utils
from api import app
from datetime import datetime


@app.route("/health", methods=["GET"])
def health():
    if request.method == "GET":
        try:
            db_utils.health_db()
            output = "database is ok"
            status = 200
        except Exception as e:
            output = str(e)
            status = 500
        return output, status


@app.route("/")
def index():
    return redirect(url_for("get_providers"))


@app.route("/get-providers", methods=["GET"])
def get_providers():
    res = db_utils.get_all_record()
    data = [{"id": x, "name": y} for x, y in res]
    return jsonify(data)


@app.route("/add-provider", methods=["GET", "POST"])
def post_provider():
    res = db_utils.insert_new_record()
    return jsonify(res)


@app.route('/provider/<id>', methods=["PUT"])
def provider_update(id):
    if request.method == "PUT":
        data = request.get_json()
        name = data['name']
        result = db_utils.edith_record_in_provider(id, name)
        return jsonify(result)


@app.route('/truck/<id>', methods = ["GET"])
def get_truck_sessions(id):
    if request.method == ("GET"):
        data = get_truck_sessions(id)
        return jsonify(data)


@app.route('/truck', methods = ["POST"])
def truck_add():
    if request.method == "POST":
        data = request.get_json()
        provider_id = data['provider_id']
        id = data['id']
        result = db_utils.add_new_reckord_in_truck(id, provider_id)
        return jsonify(result)


@app.route('/truck/<id>', methods=["PUT"])
def truck_update(id):
    if request.method == "PUT":
        data = request.get_json()
        provider_id = data['provider_id']
        result = db_utils.edith_record_in_truck(id, provider_id)
        return jsonify(result)


@app.route("/get-provider/<int:id>", methods=["GET"])
def get_provider(id):
    res = db_utils.get_record_in_provider(id)
    data = [{"id": x, "name": y} for x, y in res]
    return jsonify(data)


@app.route("/read-to-db-from-file/<filename>", methods=["GET", "POST"])
def read_to_db_from_file(filename):
    res = db_utils.save_to_db_from_file(filename)
    return jsonify(res)


@app.route("/get-rates", methods=["GET"])
def get_rates():
    res = db_utils.get_all_record_in_rates()
    data = [{"product_id": x, "rate": y, "scope": z} for x, y, z in res]
    return jsonify(data)

@app.route("/bill/<id>", methods=['GET'])
def get_bill(id):
     if request.method == ("GET"):
        bill = db_utils.create_bill()
        products = db_utils.create_products()
        sessions_count = 0
        t1 = ''
        t2 = ''

        if t1 == '':
            t1 = '000000'
        
        if t2 == '':    
            now = datetime.now().strftime("%Y%m%d%H%M%S")
            t2 = str(now)
        
        scope = db_utils.get_all_record_in_rates()

        provider = db_utils.get_record_in_provider(id)

        trucks = db_utils.get_all_trucks_of_provider(id)
        
        weights = db_utils.get_data_from_weight(t1, t2)

        for truck in trucks:
            sessions = []
            truck_datas = db_utils.get_truck_data(truck[0], t1, t2)
            for data in truck_datas:
                sessions.append(data[2])
                sessions_count += 1
            for session in sessions:
                for weight in weights:
                    if weight[0] == session:
                        for product in bill.get('products'):
                            if product.get('product') == weight.get('produce'):
                                product['amount'] += weight.get('neto')
                                product['count'] += 1
                            else:
                                products = db_utils.create_products()
                                products['name'] = weight.get('produce')
                                products['amount'] = weight.get('neto')
                                products['count'] = 1
                                bill['products'].append(products)

        for product in bill.get("products"):
            for record in scope:
                if product.get('product') == record.get('product_id') and record.get('scope') == id:
                    product['rate'] = record.get('rate')
                    product['pay'] = product.get('rate') * product.gget('amount')
                elif product.get(product) == record.get('product_id') and record.get('scope') == 'ALL':
                    product['rate'] = record.get('rate')
                    product['pay'] = product.get('rate') * product.get('amount')
            bill["total"] += product['pay']

        bill['id'] = id
        bill['name'] = provider[1]
        bill['from'] = t1
        bill['to'] = t2
        bill['trucksCount'] = len(trucks)
        bill['sessionscount'] = sessions_count
        

        return jsonify(bill)
