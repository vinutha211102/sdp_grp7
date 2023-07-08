from typing_extensions import Annotated
import typer
from food.services.food import FoodService

food = FoodService()

app = typer.Typer()


@app.command()
def add(
    name: Annotated[str, typer.Option(prompt=True)],
    price: Annotated[int, typer.Option(prompt=True)],
    quantity: Annotated[int, typer.Option(prompt=True)],
    is_veg: Annotated[bool, typer.Option(prompt=True)]
):
    food.add(name, price, quantity, is_veg)

@app.command()
def remove(name: Annotated[str, typer.Option(prompt=True)]):
    food.remove(name)


@app.command()
def display():
    food.display()