from food.models import Food
import peewee as pwee
from food.exceptions import FoodieExit
from rich.console import Console
from rich.table import Table


console = Console()

class FoodService:
    def add(self,name:str, price: int,quantity:int, is_veg: bool):
        try:
            item = Food.create(name=name, price=price, quantity=quantity,is_veg=is_veg)
        except pwee.IntegrityError:
            item: Food =Food.get(name=name)
            item.update_item(price, quantity)

    def remove(self, name:str):
        item= Food.get(name=name)
        item.delete_instance()
        print(f"{item.name} removed from food stock")  

    def display(self):
        items = Food.select()
        table = Table("sl.No.", "Name", "Price", "Avail. Quantity", "Item-id")
        for i, item in enumerate(items):
            table.add_row(
                f"{i + 1}",
                item.name,
                f"Rs. {item.price}",
                str(item.quantity),
                str(item.id),
            )

        console.print(table)

