import typer
from peewee import *
from food.models import create_tables
from food.services.authentication import UserSession, AuthenticationService
from food.services.restaurant import RestaurantService
from food.services.food import FoodService
from food.exceptions import FoodieExit

from food.commands import users, restaurant, food, cart, order

app = typer.Typer()

user_session = users.user_session
auth = users.auth

app.add_typer(users.app, name="users")
app.add_typer(restaurant.app, name="restaurant")
app.add_typer(food.app, name="food")
app.add_typer(cart.app, name="cart")
app.add_typer(order.app, name="order")


if __name__ == "__main__":
    create_tables()
    with user_session:
        try:
            auth.load_session()
            app()
        except Exception as e:
            pass