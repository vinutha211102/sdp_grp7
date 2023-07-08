from typing_extensions import Annotated
import typer
from food.services.restaurant import RestaurantService

restaurant = RestaurantService()

app = typer.Typer()


@app.command()
def add(
    name: Annotated[str, typer.Option(prompt=True)]):
    restaurant.add(name)

@app.command()
def remove(name: Annotated[str, typer.Option(prompt=True)]):
    restaurant.remove(name)


@app.command()
def display():
    restaurant.display()