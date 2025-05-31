from typing import Optional, Dict, Any
from sqlalchemy.orm import Session
from models.db.tables import UserMetadata, ProblemMetadata
from dao.connection import get_db

class UserDao:
    
 def put_user(self, username: str, email: str, created_at) -> Optional[int]:
    """
    Insert a new user into the database and create associated UserStats.

    :param username: Username of the user
    :param email: Email of the user
    :param created_at: Timestamp when the user was created
    :return: The userId of the newly created user
    """
    session = next(get_db())
    try:
        # Insert user into UserMetadata
        new_user = UserMetadata(userName=username, email=email)
        session.add(new_user)
        session.commit()
        session.refresh(new_user)  # Get the generated userId

        # Insert corresponding entry into UserStats
        new_stats = UserStats(
            userId=new_user.userId,
            totalSolved=0,
            acceptanceRate=0,
            rating=0
        )
        session.add(new_stats)
        session.commit()

        return new_user.userId
    except Exception as e:
        session.rollback()
        print("Error inserting user and stats:", e)
        return None

 def get_user_from_username_or_email(self, username: Optional[str], email: Optional[str]) -> Optional[Dict[str, Any]]:
    """
    Fetch a user by their username or email, including stats.

    :param username: Username of the user
    :param email: Email of the user
    :return: A dictionary containing user and stats details if found, else None
    """
    session = next(get_db())
    try:
        user = session.query(UserMetadata).filter(
            (UserMetadata.userName == username) | (UserMetadata.email == email)
        ).first()

        if user:
            stats = user.stats  # via relationship
            return {
                "userId": user.userId,
                "username": user.userName,
                "email": user.email,
                "totalSolved": stats.totalSolved if stats else 0,
                "acceptanceRate": stats.acceptanceRate if stats else 0,
                "rating": stats.rating if stats else 0
            }
        else:
            print(f"No user found with username: {username} or email: {email}")
            return None
    except Exception as e:
        print("Error fetching user:", e)
        return None