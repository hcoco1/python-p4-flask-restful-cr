#!/usr/bin/env python3

# Import necessary modules from the Flask library
from flask import Flask, request, make_response

# Import the Migrate module for handling database migrations
from flask_migrate import Migrate

# Import the necessary modules from Flask-RESTful for creating RESTful APIs
from flask_restful import Api, Resource

# Import the database and the Newsletter model from the models module
from models import db, Newsletter

# Create a Flask web server instance
app = Flask(__name__)

# Configure the SQLite database URI for the Flask application
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///newsletters.db'

# Disable the SQLAlchemy modification tracker to save resources
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Configure Flask to produce non-compact JSON. This makes the JSON output more readable.
app.json.compact = False

# Initialize the Migrate module with the Flask app and the database
migrate = Migrate(app, db)

# Initialize the database with the Flask app
db.init_app(app)

# Create an API object to add RESTful resources
api = Api(app)

# Define the Home resource which will handle requests to the root endpoint
class Home(Resource):

    # Define the GET method for the Home resource
    def get(self):
        
        # Create a dictionary to be returned as the response
        response_dict = {
            "message": "Welcome to the Newsletter RESTful API",
        }
        
        # Create a Flask response object with the dictionary and a 200 status code
        response = make_response(
            response_dict,
            200,
        )

        # Return the response object
        return response

# Add the Home resource to the API at the root endpoint
api.add_resource(Home, '/')

# Define the Newsletters resource to handle requests related to newsletters
class Newsletters(Resource):

    # Define the GET method to retrieve all newsletters
    def get(self):
        
        # Create a list of dictionaries representing all Newsletter records in the database
        response_dict_list = [n.to_dict() for n in Newsletter.query.all()]

        # Create a Flask response object with the list and a 200 status code
        response = make_response(
            response_dict_list,
            200,
        )

        # Return the response object
        return response

    # Define the POST method to create a new newsletter
    def post(self):
        
        # Create a new Newsletter record with the provided title and body
        new_record = Newsletter(
            title=request.form['title'],
            body=request.form['body'],
        )

        # Add the new record to the database session
        db.session.add(new_record)
        
        # Commit the changes to the database
        db.session.commit()

        # Create a dictionary representing the new record
        response_dict = new_record.to_dict()

        # Create a Flask response object with the dictionary and a 201 status code
        response = make_response(
            response_dict,
            201,
        )

        # Return the response object
        return response

# Add the Newsletters resource to the API at the /newsletters endpoint
api.add_resource(Newsletters, '/newsletters')

# Define the NewsletterByID resource to handle requests for specific newsletters by ID
class NewsletterByID(Resource):

    # Define the GET method to retrieve a newsletter by its ID
    def get(self, id):

        # Retrieve the Newsletter record by its ID and convert it to a dictionary
        response_dict = Newsletter.query.filter_by(id=id).first().to_dict()

        # Create a Flask response object with the dictionary and a 200 status code
        response = make_response(
            response_dict,
            200,
        )

        # Return the response object
        return response

# Add the NewsletterByID resource to the API at the /newsletters/<int:id> endpoint
api.add_resource(NewsletterByID, '/newsletters/<int:id>')

# Check if this script is being run as the main module
if __name__ == '__main__':
    # If so, start the Flask web server on port 5555
    app.run(port=5555)
