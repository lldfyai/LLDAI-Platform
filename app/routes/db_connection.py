# Import required library
import psycopg2
from typing import List, Tuple, Optional, Dict, Any
from config import DB_HOST, DB_NAME, DB_USER, DB_PASSWORD, DB_PORT
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

def fetch_problems_metadata(user_id: int) -> List[Dict[str, Any]]:
    try:
        # Prepare SQL query to fetch data from the ProblemMetadata table along with solvedStatus for the given user_id
        query = '''
        SELECT pm."problemId", pm."problemTitle", pm.difficulty, pm."Tags", uss."solvedStatus"
        FROM public."ProblemMetadata" pm
        LEFT JOIN public."UserSubmissionStats" uss 
        ON pm."problemId" = uss."problemId" AND uss."userId" = %s;
        '''

        # Execute the SQL command
        cursor.execute(query, (user_id,))

        # Fetch all rows from the database
        data = cursor.fetchall()

        # Return fetched data
        result = []
        for row in data:
            problem = {
                "problemId": row[0],
                "problemTitle": row[1],
                "difficulty": row[2],
                "Tags": row[3],
                "solvedStatus": row[4] if row[4] is not None else 'UNATTEMPTED'  # Default to 'UNATTEMPTED' if `solvedStatus` is None
            }
            result.append(problem)
        return result

    except Exception as e:
        print("Error: unable to fetch data", e)
        return []



def fetch_problem_metadata(user_id: int, problem_id: int) -> Optional[Dict[str, Any]]:
    try:
        # Prepare SQL query to fetch data for a specific problemId for a specific userId
        query = '''
        SELECT pm."problemId", pm."problemTitle", pm.difficulty, pm."Tags", pm.description, uss."solvedStatus"
        FROM public."ProblemMetadata" pm
        LEFT JOIN public."UserSubmissionStats" uss ON pm."problemId" = uss."problemId" AND uss."userId" = %s
        WHERE pm."problemId" = %s;
        '''

        # Execute the SQL command
        cursor.execute(query, (user_id, problem_id))

        # Fetch the row from the database
        row = cursor.fetchone()

        # If a row is found, return it as a dictionary
        if row:
            problem_metadata = {
                "problemId": row[0],
                "problemTitle": row[1],
                "difficulty": row[2],
                "Tags": row[3],
                "description": row[4],
                "solvedStatus": row[5]
            }
            return problem_metadata
        else:
            print(f"No data found for problemId: {problem_id} and userId: {user_id}")
            return None

    except Exception as e:
        print("Error: unable to fetch data", e)
        return None

def insert_problem_metadata(
        problem_title: str,
        difficulty: str,
        tags: List[str],
        time_limit: float,
        memory_limit: float,
        s3_path: str,
        description: str
) -> Optional[int]:
    try:
        insert_query = """
        INSERT INTO "ProblemMetadata" ("problemTitle", difficulty, "Tags", "timeLimit", 
                                       "memoryLimit", s3_path, description)
        VALUES (%s, %s, %s::tag[], %s, %s, %s, %s)
        RETURNING "problemId";
        """

        # Execute the query with the provided parameters
        cursor.execute(insert_query, (problem_title, difficulty, tags, time_limit,
                                      memory_limit, s3_path, description))

        # Fetch the returned problem ID
        problem_id = cursor.fetchone()[0]

        # Commit the transaction
        conn.commit()

        # Return the problem ID
        return problem_id
    except Exception as e:
        conn.rollback()
        raise e


def put_user(username: str, email: str, created_at: int):
    try:
        query = 'INSERT INTO public."UserMetadata" (username, email, created_at) VALUES (%s, %s, %s);'
        cursor.execute(query, (username, email, created_at))
        conn.commit()
    except Exception as e:
        print("Error inserting user:", e)

    finally:
        cursor.close()
        conn.close()