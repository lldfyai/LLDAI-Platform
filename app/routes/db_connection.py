# Import required library
import psycopg2
from typing import List, Tuple

# Database connection parameters
host = "m"
dbname = ""
user = ""
password = ""
port = ""

# Establish the connection
conn = psycopg2.connect(
    dbname=dbname,
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