from flask import Flask, request, jsonify
import mysql.connector
from dotenv import load_dotenv
import mysql.connector
import os
from dbq import *
from functools import wraps
import requests
from datetime import datetime
from hashlib import sha256
from flask_cors import CORS

get = os.getenv

load_dotenv()

app = Flask(__name__)
CORS(app) 

MYSQL_HOST = get("MYSQL_HOST")
MYSQL_USER = get("MYSQL_USER")
MYSQL_PSWD = get("MYSQL_PASSWORD")
MYSQL_PORT = int(get("MYSQL_PORT"))
MYSQL_DATABASE = get("MYSQL_DATABASE")
HOST = get("HOST")
PORT = int(get("PORT"))
DEBUG = get("DEBUG").lower() in  ('true', '1')
GAME_SERVICE_URL = get("GAME_API")


try: 
	database = mysql.connector.connect(
		host=MYSQL_HOST,
		user=MYSQL_USER,
		password=MYSQL_PSWD,
		database=MYSQL_DATABASE,
		port=MYSQL_PORT
	)
	print("[+] Connection successful")
except Exception as e:
	print("[!] Failed to connect to the database. Quitting...", e)
	exit(-1)


tOrder = {
	"email": "email",
	"items": "items",
	"name": "name",
	"surname": "surname",
	"address": "address"
}


# TODO request auth token, not yet JWT but think about this. Frontend  


def gameify(data):
	try:
		r = requests.post(GAME_SERVICE_URL+'/placed-order', data=data)
		
		if r.status_code in range(200, 300):
			return r.content
		else:
			print("Bad response status: ", r.status_code)
			return None
	except Exception as e:
		print(e)
		return None


@app.route('/login', methods=["POST"])	
def login():
	
	body = request.get_json()
	email = body.get("email")
	passwd = body.get("password")
	password = sha256(passwd.encode()).hexdigest()
	user = auth_user(database, email, password)
	if not user:
		return jsonify({"Invalid credentials"}), 401
	else:
		return jsonify({"user": user}), 200


@app.route('/register', methods=["POST"])
def register():
	
	body = request.get_json()
	name = body.get("name")
	surname = body.get("surname")
	email = body.get("email")
	passwd = body.get("password")
	password = sha256(passwd.encode()).hexdigest()
	id_ = register(database, name, surname, email, password)
	return jsonify({'id': id_}), 200



@app.route('/order', methods=["POST"])
#@log_access
def place_order():
	body = request.get_json()

	# check if all required parameters are in body
	req = [tOrder[key] for key in tOrder.keys()]
	missing = [x for x in req if x not in body.keys()]

	if len(missing):
		msg_ = ", ".join(missing)
		err = f"Missing required parameters {msg_}"
		print(err)
		return jsonify({'error': err}), 400

	#session = body.get(tOrder["session"])
	email = body.get(tOrder["email"])
	dishes = body.get(tOrder["items"])
	name = body.get(tOrder["name"])
	surname = body.get(tOrder["surname"])
	address = body.get(tOrder["address"])


	try: 
		idOrder = insert_order(database, dishes, {"name": name, "surname": surname, "email": email}, address)
		# res = gameify({
		# 		"User_email": email,
		# 		"level": 1,
		# 		"total_expiriance_points": 3
		# 	})

		return jsonify({'status': 'success', 'message': f'New order id {idOrder}'})
	except Exception as e:
		print(str(e))
		#print(dishes)
		return jsonify({'error': 'Something went wrong'}), 500


@app.route('/shippings', methods=["GET", "POST"])
def handle_shipment(): #rename later
	if request.method == "GET":
		try:
			res = fetch_shipped_orders(db)

			return jsonify({ "orders": res, "status": 'success'}), 200
		except Exception as e:
			print(str(e))
			return jsonify({"error": "Something went wrong"}), 500

	else:
		return jsonify({"error": "Not implemented"}), 501

@app.route('/orders/<int:oid>', methods=["GET"])
def get_order(oid):
	try:
		order = fetch_order(database, oid)
	except Exception as e:
		print(e)
		return jsonify({"Something went wrong"}), 500
	if not order:
		return jsonify({"error": f"No record matching id {oid}"}), 400

	return jsonify({"order": order}), 200


@app.route('/orders', methods=["GET"])
def get_all_orders():
	try:
		orders = fetch_orders(database)
	except Exception as e:
		print(e)
		return jsonify({"error": "Something went wrong"}), 500

	return jsonify({"orders": orders}), 200


if __name__ == "__main__":
	app.run(host="0.0.0.0", port=5000, debug=True)





