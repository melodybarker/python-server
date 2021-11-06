import sqlite3
import json
from models import Animal

ANIMALS = [
	{
		"id": 1,
		"name": "Snickers",
		"species": "Dog",
		"status": "Admitted",
		"location_id": 1,
		"customer_i-d": 4,
	},
	{
		"id": 2,
		"name": "Gypsy",
		"species": "Dog",
		"status": "Admitted",
		"location_id": 1,
		"customer_id": 2
	},
	{
		"id": 3,
		"name": "Blue",
		"species": "Cat",
		"status": "Admitted",
		"location_id": 2,
		"customer_id": 1
	}
	]


def get_all_animals():
	# Open a connection to the database
	with sqlite3.connect("./kennel.db") as conn:

		# Just use these. It's a Black Box.
		conn.row_factory = sqlite3.Row
		db_cursor = conn.cursor()

		# Write the SQL query to get the information you want
		db_cursor.execute("""
		SELECT
			a.id,
			a.name,
			a.breed,
			a.status,
			a.location_id,
			a.customer_id
		FROM animal a
		""")

		# Initialize an empty list to hold all animal representations
		animals = []

		# Convert rows of data into a Python list
		dataset = db_cursor.fetchall()

		# Iterate list of data returned from database
		for row in dataset:

			# Create an animal instance from the current row.
			# Note that the database fields are specified in
			# exact order of the parameters defined in the
			# Animal class above.
			animal = Animal(row['id'], row['name'], row['breed'],
							row['status'], row['location_id'],
							row['customer_id'])

			animals.append(animal.__dict__)

	# Use `json` package to properly serialize list as JSON
	return json.dumps(animals)


	# Function with a single parameter
def get_single_animal(id):
	with sqlite3.connect("./kennel.db") as conn:
		conn.row_factory = sqlite3.Row
		db_cursor = conn.cursor()

		# Use a ? parameter to inject a variable's value
		# into the SQL statement.
		db_cursor.execute("""
		SELECT
			a.id,
			a.name,
			a.breed,
			a.status,
			a.location_id,
			a.customer_id
		FROM animal a
		WHERE a.id = ?
		""", ( id, ))

		# Load the single result into memory
		data = db_cursor.fetchone()

		# Create an animal instance from the current row
		animal = Animal(data['id'], data['name'], data['breed'],
							data['status'], data['location_id'],
							data['customer_id'])

		return json.dumps(animal.__dict__)



def create_animal(animal):
	# Get the id value of the last animal in the list
	max_id = ANIMALS[-1]["id"]

	# Add 1 to whatever that number is
	new_id = max_id + 1

	# Add an 'id' property to the animal dictionary
	animal["id"] = new_id

	# Add the animal dictionary to the list. Append() is like push() in javascript
	ANIMALS.append(animal)

	# return the dictionary with 'id' property added
	return animal


def update_animal(id, new_animal):
    #iterate the ANIMALS list, but user enumerate() so that you can access the index value of each item
    for index, animal in enumerate(ANIMALS):
        if animal["id"] == id:
            #found the animal. update the value.
            ANIMALS[index] = new_animal
            break


def get_animals_by_location(location):
    with sqlite3.connect("./kennel.db") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        #write the sql query to get the info you want
        db_cursor.execute("""
        select
            a.id,
            a.name,
            a.breed,
            a.status,
            a.location_id,
            a.customer_id
        from Animal a
        WHERE a.location_id = ?
        """, ( location, ))

        animals=[]
        dataset = db_cursor.fetchall()

        for row in dataset:
            animal = Animal(row['id'], row['name'], row['breed'],
            row['status'], row['location_id'], row['customer_id'])
            animals.append(animal.__dict__)
    return json.dumps(animals)


def get_animals_by_status(status):
    with sqlite3.connect("./kennel.db") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        select
            a.id,
            a.breed,
            a.status,
            a.location_id,
            a.customer_id
        from Animal a
        WHERE a.status = ?
        """, ( status, ))

        animals=[]
        dataset = db_cursor.fetchall()

        for row in dataset:
            animal = Animal(row['id'], row['name'], row['breed'],
            row['status'], row['location_id'], row['customer_id'])
            animals.append(animal.__dict__)
    return json.dumps(animals)


def delete_animal(id):
    with sqlite3.connect("./kennel.db") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        DELETE FROM animal
        WHERE id = ?
        """, (id, ))