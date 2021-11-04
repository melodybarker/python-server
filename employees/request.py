import sqlite3
import json
from models import Employee


EMPLOYEES = [
	{
		"id": 1,
		"name": "Emma Beaton",
		"address": "111 Okay St.",
		"location_id": 1
	},
	{
		"id": 2,
		"name": "Lee Crumbs",
		"address": "321 Beach View",
		"location_id": 2
	},
	{
		"id": 3,
		"name": "Jeremy Bakker",
		"address": "7890 Pizza Palace",
		"location_id": 2
	}
]


def get_all_employees():
	#open a connection to the database
	with sqlite3.connect("./kennel.db") as conn:

		#black box
		conn.row_factory = sqlite3.Row
		db_cursor = conn.cursor()

		#write the sql query to get the info you want
		db_cursor.execute("""
		SELECT
			e.id,
			e.name,
			e.address,
			e.location_id
		FROM employee e
		""")

		#initialize an empty list to hold all animal representations
		employees = []

		#convert rows of data into a python list
		dataset = db_cursor.fetchall()

		#iterate list of data returned from database
		for row in dataset:

			#create a customer instance from the current row.
			#note that the database fields are specified in exact order
			#of the parameters defined in the Customer class above.
			employee = Employee(row['id'], row['name'],
								row['address'], row['location_id'])
			employees.append(employee.__dict__)

	#use 'json' package to properly serialize list as JSON
	return json.dumps(employees)


def get_single_employee(id):
	with sqlite3.connect("./kennel.db") as conn:
		conn.row_factory = sqlite3.Row
		db_cursor = conn.cursor()

		#use a ? parameter to inject a variable's value into sql statement
		db_cursor.execute("""
		SELECT
			e.id,
			e.name,
			e.address,
			e.location_id
		FROM employee e
		WHERE e.id = ?
		""", ( id, ))

		#load the single result into memory
		data = db_cursor.fetchone()
		#create employee instance from current row
		employee = Employee(data['id'], data['name'],
							data['address'], data['location_id'])

		return json.dumps(employee.__dict__)


def create_employee (employee):
	max_id = EMPLOYEES[-1]["id"]
	new_id = max_id + 1
	employee["id"] = new_id
	EMPLOYEES.append(employee)
	return employee


def delete_employee(id):
	employee_index = -1
	for index, employee in enumerate(EMPLOYEES):
		if employee["id"] == id:
			employee_index = index
	if employee_index >= 0:
		EMPLOYEES.pop(employee_index)


def update_employee(id, new_employee):
	for index, employee in enumerate(EMPLOYEES):
		if employee ["id"] == id:
			EMPLOYEES[index] = new_employee
			break