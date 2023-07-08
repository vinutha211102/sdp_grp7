from food.models import Restaurant
import peewee as pwee
from rich.console import Console
from rich.table import Table

console = Console()

class RestaurantService:
    def add(self, name:str):
        res_name=Restaurant.create(name=name)
        print(f"{res_name.name} added to Restaurants")

    def remove(self,name:str):
        res_name= Restaurant.get(name=name)
        res_name.delete_instance()
        print(f"{res_name} removed from Restaurants")

    def display(self):
        res_names=Restaurant.select()
        table=Table("sl no.",
                    "name")
        for i,res_name in enumerate(res_names):
            table.add_row(f"{i+1}",
                          res_name.name,)

        console.print(table)



