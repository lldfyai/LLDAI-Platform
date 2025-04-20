from typing import Optional, Dict, Any
from sqlalchemy.orm import Session
from models.db.tables import UserMetadata, ProblemMetadata
from dao.connection import get_db

class UserDao:
    
    def put_user(self, username: str, email: str, created_at) -> Optional[int]:
        """
        Insert a new user into the database.

        :param username: Username of the user
        :param email: Email of the user
        :param created_at: Timestamp when the user was created
        :return: The userId of the newly created user
        """
        session = next(get_db())
        try:
            new_user = UserMetadata(username=username, email=email, created_at=created_at)
            session.add(new_user)
            session.commit()
            session.refresh(new_user)  # Refresh to get the generated userId
            return new_user.userId
        except Exception as e:
            session.rollback()
            print("Error inserting user:", e)
            return None

    def get_user_from_username_or_email(self, username: Optional[str], email: Optional[str]) -> Optional[Dict[str, Any]]:
        """
        Fetch a user by their username or email.

        :param username: Username of the user
        :param email: Email of the user
        :return: A dictionary containing user details if found, else None
        """
        session = next(get_db())
        try:
            user = session.query(UserMetadata).filter(
                (UserMetadata.username == username) | (UserMetadata.email == email)
            ).first()

            if user:
                return {
                    "userId": user.userId,
                    "username": user.username,
                    "email": user.email,
                    "problemsSolved": user.problemssolved,
                    "rank": user.rank
                }
            else:
                print(f"No user found with username: {username} or email: {email}")
                return None
        except Exception as e:
            print("Error fetching user:", e)
            return None