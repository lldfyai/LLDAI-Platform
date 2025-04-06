from datetime import datetime
from dao.user_dao import UserDao

class UserManager:
    def __init__(self):
        self.user_dao = UserDao()

    def create_user(self, username: str, email: str) -> int:
        """
        Create a new user in the database.

        :param username: Username of the user
        :param email: Email of the user
        :return: The userId of the newly created user
        """
        created_at = datetime.utcnow()  # Get the current UTC timestamp
        user_id = self.user_dao.put_user(username, email, created_at)
        if not user_id:
            raise Exception("Failed to create user")
        return user_id

    def get_user(self, username: str = None, email: str = None) -> dict:
        """
        Retrieve a user by their username or email.

        :param username: Username of the user
        :param email: Email of the user
        :return: A dictionary containing user details if found
        """
        user_details = self.user_dao.get_user_from_username_or_email(username, email)
        if not user_details:
            raise Exception("User not found")
        return user_details