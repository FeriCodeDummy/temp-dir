def auth_user(database, email, password):
	cursor = database.cursor()
	sql = "SELECT idUser, name, surname from Users where email = %s and password = %s;"
	cursor.execute(sql, (email, password))
	data = cursor.fetchall()
	if not len(data):
		return None
	
	r= data[0]
	return ({"id": r[0], "name": r[1], "surname": r[2], "email":email})


def register(db, name, surname, email, password):
	cursor = db.cursor()
	
	sql = "insert into Users VALUES (NULL, %s, %s, %s, %s);"
	cursor.execute(sql, (name, surname, email, password))
	db.commit()

	return cursor.lastrowid



def insert_order(db, items, user, address):
	cursor = db.cursor()

	names = "', '".join([x["name"] for x in items])
	sqlii = f"SELECT idItem, price from Items WHERE name in ('{names}');"

	cursor.execute(sqlii)
	results_ii = []

	# Optionally, fetch additional data from menu 

	res_ii = cursor.fetchall()
	for i, item in enumerate(res_ii):
		results_ii.append({
			"id": item[0],
			"quantity": items[i]["quantity"]
		})



	sql_u = "SELECT idCustomer from Customers WHERE email = %s;"
	cursor.execute(sql_u, (user["email"], ))
	res = cursor.fetchone()
	if len(res) == 0: # new customer 
		sql_iu = "INSERT INTO Customers (`name`, `surname`, `email`) VALUES (%s, %s, %s);"
		cursor.execute(sql, (user["name"], user["surname"], user["email"]))
		db.commit()
		id_ = cursor.lastrowid
	else:
		id_ = res[0]
	

	sql = "INSERT INTO Orders(`idOrder`, `status`, `shipping_address`, `fk_customer`) VALUES (NULL, 'placed', %s, %s);"
	cursor.execute(sql, (address, id_ ))
	db.commit()
	idOrder = cursor.lastrowid

	print(idOrder)


	injection = []
	for i in results_ii: 
		injection.append(f"({idOrder}, {i['id']}, {i['quantity']})")

	injection = ', '.join(injection)


	sql_it  = f"INSERT INTO order_has_item(`fk_order`, `fk_item`, `quantity`) VALUES {injection}";
	cursor.execute(sql_it)
	db.commit()

	return idOrder
	
	
def fetch_shipped_orders(db):
	cursor = db.cursor()

	sql = """ 
		SELECT c.Name, c.Surname, c.Email, COUNT(idOrder), SUM(price) FROM Orders
			JOIN Customers c on fk_customer = idCustomer
			JOIN order_has_item ON fk_order = idOrder
			JOIN Items on fk_item = idItem
		GROUP BY idOrder
		WHERE status = `payed`;
	"""

	cursor.execute(sql)

	res = cursor.fetchall()

	resultt = [] 

	for row in res:
		resultt.append({
			"name": row[0],
			"surname": row[1],
			"email": row[2],
			"quantity": row[3],
			"price": row[4]
		})

	return resultt


def fetch_order(db, oid):
	cursor = db.cursor()
	sql = """ 
		SELECT I.name, I.price, c.name, c.surname, c.email, ohi.quantity, o.placed_at from Items I 
			JOIN order_has_item ohi ON fk_item = idItem 
		    JOIN Orders o on idOrder = fk_order
		    JOIN Customers c ON fk_customer = idCustomer
    WHERE fk_order = %s
	"""
	cursor.execute(sql, (oid, ))

	res = cursor.fetchall()

	if not len(res) > 0:
		return None 
	
	user = {
		"name": res[0][2],
		"surname": res[0][3],
		"email": res[0][4]
	}

	order = {
		"id": oid,
		"customer": user,
		"items": [],
		"placed_at": res[0][6]
	}

	for item in res:
		order["items"].append({
			"name": item[0],
			"price": item[1],
			"quantity": item[5]
		})

	return order
