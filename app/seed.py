from flask import Flask
from random import randint, choice as rc
from flask_sqlalchemy import SQLAlchemy
from app import app
from faker import Faker

from models import db, Restaurant, Pizza, RestaurantPizza

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

fake = Faker()

pizza_name = [
    "Chessy Chicken",
    "Chicken BBQ",
    "Cheeseburger",
    "Meaty BBQ",
    "Pepperoni",
    "Super Meaty",
    "Shawarma",
    "Chicken Supreme",
    "Dodo Supreme",
    "Spicy Mixed Pizza",
]

pizza_ingredient = [
    "Cheese",
    "Plantain",
    "Beef",
    "Chili",
    "Suya",
    "Veggie",
    "Chicken",
    "Grilled Eggplant",
    "Grilled Pineapple",
    "Garlic",
    "Onions",
    "Jalapeños",
    "Capers",
    "Cashew Cream",
    "Balsamic Glaze",
    "Shawarma",
    "Tomatoes",
    "Red Pepper",
    "Broccoli",
    "Roasted Fennel",
    "Cauliflower",
    "Mushrooms",
]

# # Import the necessary SQLAlchemy models from your models.py file

with app.app_context():
    
    # Used to reset the db, deletes any previoue info on the db any time this file is initiated
    Restaurant.query.delete()
    Pizza.query.delete()
    RestaurantPizza.query.delete()
    

    # Generate fake restaurant data
    restaurants = []
    for value in range(10):
        restaurant = Restaurant(
            name=fake.company(), 
            address=fake.address(),
            )
        restaurants.append(restaurant)

    db.session.add_all(restaurants)

    # Generate fake pizza data
    pizzas = []
    for value in range(10):
        
        pizza = Pizza(
            name=pizza_name[value],
            ingredients=', '.join(rc(pizza_ingredient, k=3)),
            )
        pizzas.append(pizza)

    db.session.add_all(pizzas)

    # Generate and add fake restaurants and pizzas relationships 
    restaurant_pizzas = []
    for value in range(40):
        restaurant_pizza = RestaurantPizza(
            price = randint(1, 30)            
        ) 
        restaurant_pizza.pizza = rc(pizzas)
        restaurant_pizza.restaurant = rc(restaurants)

        restaurant_pizzas.append(restaurant_pizza)
    db.session.add_all(restaurant_pizzas)
    
    # Commit the changes to the database
    # db.session.commit()

if __name__ == '__main__':
    app.run()


