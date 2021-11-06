import sqlite3
import json
from models import Location


LOCATIONS = [
	{
		"id": 1,
		"location": "Nashville Kennel North",
		"address": "8422 Johnson Pike"
	},
	{
		"id": 2,
		"location": "Nashville Kennel South",
		"address": "209 Emory Drive"
	}
]


def get_all_locations():
	# Open a connection to the database
	with sqlite3.connect("./kennel.db") as conn:

		# Just use these. It's a Black Box.
		conn.row_factory = sqlite3.Row
		db_cursor = conn.cursor()

		# Write the SQL query to get the information you want
		db_cursor.execute("""
		SELECT
			l.id,
			l.name,
            l.address
		FROM location l
		""")

		# Initialize an empty list to hold all animal representations
		locations = []

		# Convert rows of data into a Python list
		dataset = db_cursor.fetchall()

		# Iterate list of data returned from database
		for row in dataset:

			# Create an animal instance from the current row.
			# Note that the database fields are specified in
			# exact order of the parameters defined in the
			# Animal class above.
			location = Location(row['id'], row['name'], row['address'])

			locations.append(location.__dict__)

		# Use `json` package to properly serialize list as JSON
		return json.dumps(locations)


def get_single_location(id):
	with sqlite3.connect("./kennel.db") as conn:
		conn.row_factory = sqlite3.Row
		db_cursor = conn.cursor()

		# Use a ? parameter to inject a variable's value
		# into the SQL statement.
		db_cursor.execute("""
		SELECT
			l.id,
			l.name,
			l.address
		FROM location l
		WHERE l.id = ?
		""", ( id, ))

		# Load the single result into memory
		data = db_cursor.fetchone()

		# Create an animal instance from the current row
		location = Location(data['id'], data['name'], data['address'])

		return json.dumps(location.__dict__)


def create_location(location):
	max_id = LOCATIONS[-1]["id"] #get id value of the last location in list
	new_id = max_id + 1 # add 1 to the last ID in the list
	location["id"] = new_id # add an "id" property to location dictionary
	LOCATIONS.append(location) # add loation dictionary to list.
	return location # return the dictionary with "id" property added


def delete_location(id):
	location_index = -1 #initial -1 value for location index, in case one isn't found
	for index, location in enumerate(LOCATIONS): #iterate the LOCATIONS list, but use enumerate() so that you can access the index value of each item
		if location["id"] == id:
			location_index = index #found the location. Store the current index.
	if location_index >= 0:
		LOCATIONS.pop(location_index) #if the location was found, use pop(int) to remove it from list


def update_location(id, new_location):
	for index, location in enumerate(LOCATIONS):
		if location["id"] == id:
			LOCATIONS[index] = new_location
			break
