# Import required library
import psycopg2
from typing import List, Tuple
from app.config import DB_HOST, DB_NAME, DB_USER, DB_PASSWORD, DB_PORT
from sqlalchemy import create_engine, Column, Integer, String, BigInteger

# Database connection parameters
host = DB_HOST
dbname = DB_NAME
user = DB_USER
password = DB_PASSWORD
port = DB_PORT

# Establish the connection
conn = psycopg2.connect(
    dbname="lldfy_db",
    user=user,
    password=password,
    host=host,
    port=port
)

# Create a cursor object using the cursor() method
cursor = conn.cursor()

def fetch_problems_metadata() -> List[Tuple[int, str, str, list]]:
    try:
        # Prepare SQL query to fetch data from the problemMetadata table
        query = query = 'SELECT "problemId", "problemTitle", difficulty, "Tags" FROM public."ProblemMetadata";'

        # Execute the SQL command
        cursor.execute(query)

        # Fetch all rows from the database
        data = cursor.fetchall()

        # Return fetched data
        return data

    except Exception as e:
        print("Error: unable to fetch data", e)
        return []

    finally:
        # Close the database connection
        if conn is not None:
            conn.close()

def put_user(userName: str, email: str):
    try:
        # Quote the column "userName" to preserve the case
        query = 'INSERT INTO public."UserMetadata" ("userName", email) VALUES (%s, %s);'
        cursor.execute(query, (userName, email))
        conn.commit()
    except Exception as e:
        print("Error inserting user:", e)
    finally:
        cursor.close()
        conn.close()