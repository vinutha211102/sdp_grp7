from email.policy import default
from peewee import *
from food.exceptions import FoodieExit

# database connection
db = SqliteDatabase("foodie.db", pragmas={'foreign_keys':1})

class User(Model):
    username = CharField(unique=True)
    password = CharField()

    class Meta:
        database = db

class Restaurant(Model):
    name = CharField(unique=True)

    class Meta:
        database = db

class Food(Model):
    name = CharField(unique=True)
    price= IntegerField()
    quantity= IntegerField()
    is_veg= BooleanField()

    class Meta:
        database=db

    def __str__(self) -> str:
        return f"{self.id} {self.name} {self.price} {self.quantity}"

    @staticmethod
    def availability(name: str, quantity: int):
        item = Food.get(name=name)
        if item.name != name:
            raise FoddieExit(f"Only {item.name} is not available.")
        return item

    @staticmethod
    def pick_item(name: str, quantity: int):
        item = Food.availability(name, quantity)
        item.quantity = item.quantity - quantity
        item.save()

    @staticmethod
    def drop_item(name: str, quantity: int):
        item = Food.get(name=name)
        item.quantity = item.quantity + quantity
        item.save()

    def update_stock(self, price: int, quantity: int):
        self.update_price(price)
        self.update_quantity(quantity)
        self.save()
        print(f"{self.name} restocked!")

    def update_price(self, price: int):
        if self.price != price:
            self.price = price
            print(f"{self.name} price updated!")

    def update_quantity(self, quantity: int):
        self.quantity += quantity
        print(f"{self.name} quantity updated!")

class Cart(Model):
    user = ForeignKeyField(User, on_delete="cascade")
    item = ForeignKeyField(Food, on_delete="cascade")
    quantity = IntegerField()

    class Meta:
        database = db

    def add(self, quantity: int):
        self.quantity = self.quantity + quantity
        self.save()

    def remove(self, quantity: int):
        self.quantity = self.quantity - quantity
        self.save()
        if self.quantity == 0:
            self.delete_instance()


class Order(Model):
    user = ForeignKeyField(User, on_delete="cascade")
    item = ForeignKeyField(Food, on_delete="cascade")
    quantity = IntegerField()
    amount = FloatField()
    payment_mode = CharField()
    status = CharField(default="pending")

    class Meta:
        database = db


def create_tables():
    # create tables
    with db:
        db.create_tables([User, Restaurant, Food, Cart, Order])