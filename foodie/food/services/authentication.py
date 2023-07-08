import os
import json
from food.exceptions import FoodieExit
from food.models import User, Restaurant, Food
import peewee as pwee


class UserSession:
    """
    UserSession class saves the current logged in user in a session file
    and loads it when needed to avoid multiple logins for each command.
    """

    session_file = "./foodie.session"

    def __init__(self):
        self.current_user = None

    def __enter__(self):
        if os.path.exists(self.session_file):
            with open(self.session_file, "r") as file:
                session_data = json.load(file)
                self.current_user = session_data.get("current_user")
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        session_data = {"current_user": self.current_user}
        with open(self.session_file, "w") as file:
            json.dump(session_data, file)
        self.current_user = None

    def set_current_user(self, user):
        # set current user to session
        self.current_user = user


class AuthenticationService:
    user = None

    def __init__(self, session: UserSession) -> None:
        self.session = session

    def list_users(self):
        users = User.select()
        for i, u in enumerate(users):
            print(f"{i+1}. {u.username}")

    def is_authenticated(self):
        if self.session.current_user is None:
            raise FoodieExit("User is not logged in.")

    def signup(self, username: str, password: str):
        try:
            user = User.create(username=username, password=password)
        except pwee.IntegrityError as e:
            raise FoodieExit(f"User '{username}' already exists.") from e

    def login(self, username: str, password: str):
        try:
            user = User.get(username=username, password=password)
            self.session.set_current_user(user.username)
        except pwee.DoesNotExist as e:
            raise FoodieExit("Check username and password") from e

    def load_session(self):
        if self.session.current_user is not None:
            try:
                self.user = User.get(username=self.session.current_user)
            except:
                raise FoodieExit("something went wrong, login again") 

    def logout(self):
        with self.session:
            print(
                f"Thank you for shopping, {self.session.current_user}! See you soon, bye."
            )