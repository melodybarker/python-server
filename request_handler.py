from http.server import BaseHTTPRequestHandler, HTTPServer
import json

from animals import (
    get_all_animals,
    get_single_animal,
    create_animal,
    delete_animal,
    update_animal
)
from customers import (
    get_all_customers,
    get_single_customer,
    create_customer,
    delete_customer,
    update_customer
)
from employees import (
    get_all_employees,
    get_single_employee,
    create_employee,
    delete_employee,
    update_employee
)
from locations import (
    get_all_locations,
    get_single_location,
    create_location,
    delete_location,
    update_location
)


# Here's a class. It inherits from another class.
# For now, think of a class as a container for functions that
# work together for a common purpose. In this case, that
# common purpose is to respond to HTTP requests from a client.
class HandleRequests(BaseHTTPRequestHandler):

    def parse_url(self, path):
        # Just like splitting a string in JavaScript. If the
        # path is "/animals/1", the resulting list will
        # have "" at index 0, "animals" at index 1, and "1"
        # at index 2.
        path_params = path.split("/")
        resource = path_params[1]
        id = None
        # Try to get the item at index 2
        try:
        # Convert the string "1" to the integer 1
        # This is the new parseInt()
            id = int(path_params[2])
        except IndexError:
            pass  # No route parameter exists: /animals
        except ValueError:
            pass  # Request had trailing slash: /animals/
        return (resource, id)  # This is a tuple

	# Here's a class function
    def _set_headers(self, status):
        self.send_response(status)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

	# Another method! This supports requests with the OPTIONS verb.
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods','GET, POST, PUT, DELETE')
        self.send_header('Access-Control-Allow-Headers','X-Requested-With',  'Content-Type', 'Accept')
        self.end_headers()

        # Here's a method on the class that overrides the parent's method.
        # It handles any GET request.
    def do_GET(self):
        self._set_headers(200)
        response = {}  # Default response

        # Parse the URL and capture the tuple that is returned
        (resource, id) = self.parse_url(self.path)

        if resource == "animals":
            if id is not None:
                response = f"{get_single_animal(id)}"
            else:
                response = f"{get_all_animals()}"

        elif resource == "locations":
            if id is not None:
                response = f"{get_single_location(id)}"
            else:
                response = f"{get_all_locations()}"

        elif resource == "employees":
            if id is not None:
                response = f"{get_single_employee(id)}"
            else:
                response = f"{get_all_employees()}"

        elif resource == "customers":
            if id is not None:
                respone = f"{get_single_customer(id)}"
            else:
                response = f"{get_all_customers()}"

        self.wfile.write(response.encode())

    # Here's a method on the class that overrides the parent's method.
    # It handles any POST request.

    def do_POST(self):
        self._set_headers(201)
        content_len = int(self.headers.get('content-length', 0))
        post_body = self.rfile.read(content_len)

        # Convert JSON string to a Python dictionary
        post_body = json.loads(post_body)

        # Parse the URL
        (resource, id) = self.parse_url(self.path)

        # Initialize new animal
        new_animal = None

        # Add a new animal to the list. Don't worry about
        # the orange squiggle, you'll define the create_animal
        # function next.
        if resource == "animals":
            new_animal = create_animal(post_body)

        # Encode the new animal and send in response
        self.wfile.write(f"{new_animal}".encode())

        new_location = None
        if resource == "locations":
            new_location = create_location(post_body)
        self.wfile.write(f"{new_location}".encode())

        new_employee = None
        if resource == "employees":
            new_employee = create_employee(post_body)
        self.wfile.write(f"{new_employee}".encode())

        new_customer = None
        if resource == "customers":
            new_customer = create_customer(post_body)
        self.wfile.write(f"{new_customer}".encode())

    def do_DELETE(self):
        # Set a 204 response code
        self._set_headers(204)

        # Parse the URL
        (resource, id) = self.parse_url(self.path)

        # Delete a single animal from the list
        if resource == "animals":
            delete_animal(id)
        self.wfile.write("".encode())
        if resource == "customers":
            delete_customer(id)
        self.wfile.write("".encode())
        if resource == "employees":
            delete_employee(id)
        self.wfile.write("".encode())
        if resource == "locations":
            delete_location(id)
        self.wfile.write("".encode()) # Encode the new location and send in response


    # Here's a method on the class that overrides the parent's method.
    # It handles any PUT request.
    def do_PUT(self):
        self._set_headers(204)
        content_len = self.rfile.read('content-length', 0)
        post_body = self.rfile.read(content_len)
        post_body = json.loands(post_body)

        (resource, id) = self.parse_url(self.path) #parse the url
        if resource == "animals":
            update_animal(id, post_body) #delete a single animal from the list
        elif resource == "customers":
            update_customer(id, post_body)
        elif resource == "employees":
            update_employee(id, post_body)
        elif resource == "locations":
            update_location(id, post_body)
        self.wfile.write("".encode()) #encode the new item and send in response

# This function is not inside the class. It is the starting
# point of this application.
def main():
    host = ''
    port = 8088
    HTTPServer((host, port), HandleRequests).serve_forever()


if __name__ == "__main__":
    main()