import sqlite3
import json
from models import Customer


CUSTOMERS = [
	{
		"id": 1,
		"name": "Hannah Hall",
		"address": "7002 Chestnut Ct",
		"pet_id": 1
	},
	{
		"id": 2,
		"name": "Mike Mullin",
		"address": "1204 Oakland Dr",
		"pet_id": 2
	},
	{
		"id": 3,
		"name": "Faye Stevens",
		"address": "358 West Willow St",
		"pet_id": 3
	}
]


def get_all_customers():
	#open a connection to the database
	with sqlite3.connect("./kennel.db") as conn:

		#black box
		conn.row_factory = sqlite3.Row
		db_cursor = conn.cursor()

		#write the sql query to get the info you want
		db_cursor.execute("""
		SELECT
			c.id,
			c.name,
			c.address,
			c.email,
			c.password
		FROM customer c
		""")

		#initialize an empty list to hold all customer representations
		customers = []

		#convert rows of data into a python list
		dataset = db_cursor.fetchall()

		#iterate list of data returned from database
		for row in dataset:

			#create a customer instance from the current row.
			#note that the database fields are specified in exact order
			#of the parameters defined in the Customer class above.
			customer = Customer(row['id'], row['name'],
								row['address'], row['email'], row['password'])
			customers.append(customer.__dict__)

		#use 'json' package to properly serialize list as JSON
	return json.dumps(customers)


def get_single_customer(id):
	with sqlite3.connect("./kennel.db") as conn:
		conn.row_factory = sqlite3.Row
		db_cursor = conn.cursor()

		#use a ? parameter to inject a variable's value into the sql statement.
		db_cursor.execute("""
		SELECT
			c.id,
			c.name,
			c.address,
			c.email,
			c.password
		FROM customer c
		WHERE c.id = ?
		""", ( id, ))

		#load the single result into memory
		data = db_cursor.fetchone()

		#create a customer instance from the current row
		customer = Customer(data['id'], data['name'],
							data['address'], data['email'], data['password'])
		return json.dumps(customer.__dict__)


def create_customer(customer):
	max_id = CUSTOMERS[-1]["id"]
	new_id = max_id + 1
	customer["id"] = new_id
	CUSTOMERS.append(customer)
	return customer


def delete_customer(id):
	customer_index = -1
	for index, customer in enumerate(CUSTOMERS):
		if customer["id"] == id:
			customer_index = index
	if customer_index >= 0:
		CUSTOMERS.pop(customer_index)


def update_customer(id, new_customer):
	for index, customer in enumerate(CUSTOMERS):
		if customer["id"] == id:
			CUSTOMERS[index] = new_customer
			break


def get_customers_by_email(email):

    with sqlite3.connect("./kennel.db") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        db_cursor.execute("""
        select
            c.id,
            c.name,
            c.address,
            c.email,
            c.password
        from Customer c
        WHERE c.email = ?
        """, ( email, ))

        customers = []
        dataset = db_cursor.fetchall()

        for row in dataset:
            customer = Customer(row['id'], row['name'], row ['address'], row['email'] , row['password'])
            customers.append(customer.__dict__)

    return json.dumps(customers)