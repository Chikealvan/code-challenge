#!/usr/bin/env python3

from flask import Flask, request, make_response, jsonify
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

from models import db, Restaurant, Pizza, RestaurantPizza

# Create the Flask app
app = Flask(__name__)

# Configure the app for SQLAlchemy and migrations
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False
CORS(app)
migrate = Migrate(app, db)

# Initialize the database
db.init_app(app)

# Route for home testing
@app.route('/')
def home_testing():
    return "<h1>Hint: Delete the H1 after testing.</h1>"

# Route for handling both GET and DELETE requests to '/restaurants'
@app.route('/restaurants', methods=['GET', 'DELETE'])
def get_and_delete_restaurant():
    if request.method == 'GET':
        # Extract the 'id' parameter from the request args
        id = request.args.get('id')
        # Query the restaurant by id
        restaurant = Restaurant.query.get(id)

        if restaurant is None:
            return jsonify({'error': 'Restaurant not found'}), 404

        # Build the response data for GET request
        pizzas = []
        for restaurant_pizza in restaurant.pizzas:
            pizza = restaurant_pizza.pizza
            pizza_data = {
                'id': pizza.id,
                'name': pizza.name,
                'ingredients': pizza.ingredients
            }
            pizzas.append(pizza_data)

        restaurant_data = {
            'id': restaurant.id,
            'name': restaurant.name,
            'address': restaurant.address,
            'pizzas': pizzas
        }

        return jsonify(restaurant_data)

    elif request.method == 'DELETE':
        # Extract the 'id' parameter from the request args
        id = request.args.get('id')
        # Query the restaurant by id
        restaurant = Restaurant.query.get(id)

        if restaurant is None:
            return jsonify({'error': 'Restaurant not found'}), 404

        # Delete the restaurant and commit changes to the database
        db.session.delete(restaurant)
        db.session.commit()

        return make_response('', 200)

# Route for handling POST requests to '/restaurants'
@app.route('/restaurants', methods=['POST'])
def create_restaurant():
    data = request.get_json()

    name = data.get('name')
    address = data.get('address')

    if not name or not address:
        return jsonify({'errors': ['Missing required data']}), 400

    # Create a new restaurant
    restaurant = Restaurant(name=name, address=address)
    db.session.add(restaurant)
    db.session.commit()

    # Build the response data
    response_data = {
        'id': restaurant.id,
        'name': restaurant.name,
        'address': restaurant.address
    }

    return make_response(jsonify(response_data), 201)

# Route for handling PUT requests to '/restaurants/<int:id>'
@app.route('/restaurants/<int:id>', methods=['PUT'])
def update_restaurant(id):
    data = request.get_json()

    # Query the restaurant by id
    restaurant = Restaurant.query.get(id)

    if restaurant is None:
        return jsonify({'error': 'Restaurant not found'}), 404

    # Update restaurant details
    restaurant.name = data.get('name', restaurant.name)
    restaurant.address = data.get('address', restaurant.address)

    # Commit changes to the database
    db.session.commit()

    return make_response(jsonify({'message': 'Restaurant updated'}), 200)

# Route for handling GET requests to '/pizzas'    
@app.route('/pizzas', methods=['GET'])
def get_pizzas():
    # Retrieve all pizzas from the database
    pizzas = Pizza.query.all()

    # Build the response data
    response_data = [pizza.to_dict() for pizza in pizzas]

    return make_response(jsonify(response_data), 200)

# Run the app if this script is executed
if __name__ == '__main__':
    app.run(port=5555, debug=True)



# from flask import Flask, request, make_response, jsonify
# from flask_migrate import Migrate
# from flask_sqlalchemy import SQLAlchemy
# from flask_cors import CORS

# from models import db, Restaurant, Pizza, RestaurantPizza

# app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.json.compact = False
# CORS(app)
# migrate = Migrate(app, db)

# db.init_app(app)

# @app.route('/')
# def home_testing():
#     return "<h1>Hint: Delete the H1 after testing.</h1>"

# @app.route('/restaurants', methods=['GET'])
# def get_restaurants():
#     # Retrieve all restaurants from the database
#     restaurants = Restaurant.query.all()

#     # Format the data using a list comprehension and to_dict method
#     restaurant_list = [restaurant.to_dict(rules=('-pizzas',)) for restaurant in restaurants]
#     response = make_response(
#         jsonify(restaurant_list),
#         200
#     )
    
# # Define a route for handling GET requests to '/restaurants/<int:id>'
# @app.route('/restaurants/<int:id>', methods=['GET', 'DELETE'])
# def get_restaurants(id):
#     restaurant = Restaurant.query.filter(Restaurant.id == id).first()

#     if restaurant is None:
#         return jsonify({'error': 'Restaurant not found'}), 404 
#     response = make_response(jsonify(restaurant.to_dict()), 200)
#     return response

# # Define a route for handling POST requests to '/restaurants'
# @app.route('/restaurants', methods=['POST'])
# def create_restaurant():
#     data = request.get_json()

#     name = data.get('name')
#     address = data.get('address')

#     if not name or not address:
#         return jsonify({'errors': ['Missing required data']}), 400

#     restaurant = Restaurant(name=name, address=address)
#     db.session.add(restaurant)
#     db.session.commit()

#     response = make_response(
#         jsonify([restaurant.to_dict(rules=('-pizzas',)) for restaurant in [restaurant]]), 200
#     )
#     return response

# # Define a route for handling POST requests to '/restaurants'
# @app.route('/restaurants', methods=['POST'])
# def create_restaurant():
#     data = request.get_json()

#     name = data.get('name')
#     address = data.get('address')

#     if not name or not address:
#         return jsonify({'errors': ['Missing required data']}), 400

#     restaurant = Restaurant(name=name, address=address)
#     db.session.add(restaurant)
#     db.session.commit()

#     response = make_response(
#         jsonify([restaurant.to_dict(rules=('-pizzas',)) for restaurant in [restaurant]]),
#         200
#     )
#     return response


# # Define a route for handling PUT requests to '/restaurants/<int:id>'
# @app.route('/restaurants/<int:id>', methods=['PUT'])
# def update_restaurant(id):
#     data = request.get_json()

#     restaurant = Restaurant.query.get(id)

#     if restaurant is None:
#         return jsonify({'error': 'Restaurant not found'}), 404

#     restaurant.name = data.get('name', restaurant.name)
#     restaurant.address = data.get('address', restaurant.address)

#     db.session.commit()
#     response = make_response(
#         jsonify({'message': 'Restaurant updated'}),
#         200
#     )
#     return response


# # Define a route for handling DELETE requests to '/restaurants/<int:id>'
# @app.route('/restaurants/<int:id>', methods=['DELETE'])
# def delete_restaurant(id):
#     restaurant = Restaurant.query.get(id)

#     if restaurant is None:
#         return jsonify({'error': 'Restaurant not found'}), 404

#     db.session.delete(restaurant)
#     db.session.commit()
#     return make_response('', 200)


# # Define a route for handling GET requests to '/pizzas'    
# @app.route('/pizzas', methods=['GET'])
# def get_pizzas():
#     # Retrieve all pizzas from the database
#     pizzas = Pizza.query.all()
#     response = make_response(
#         jsonify([pizza.to_dict() for pizza in pizzas]),
#         200
#     )
#     return response

# if __name__ == '__main__':
#     app.run(port=5555, debug=True)


