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
	return LOCATIONS


def get_single_location(id):
	requested_location = None

	for location in LOCATIONS:
		if location["id"] == id:
			requested_location = location

	return requested_location


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
