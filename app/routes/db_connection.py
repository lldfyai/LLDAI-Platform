# Import required library
import psycopg2
from typing import List, Tuple, Optional, Dict, Any

# Database connection parameters
host = "lldfy-db.cxqsgsoe4cua.us-west-2.rds.amazonaws.com"
dbname = "lldfy_db"
user = "admin_user"
password = "Blockbuster123"
port = "5432"

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
        result = []
        for row in data:
            problem = {
                "problemId": row[0],
                "problemTitle": row[1],
                "difficulty": row[2],
                "Tags": row[3]
            }
            result.append(problem)
        return result

    except Exception as e:
        print("Error: unable to fetch data", e)
        return []


def fetch_problem_metadata(problem_id: int) -> Optional[Dict[str, Any]]:
    try:
        # Prepare SQL query to fetch data for a specific problemId
        query = '''
        SELECT "problemId", "problemTitle", difficulty, "Tags", "description"
        FROM public."ProblemMetadata"
        WHERE "problemId" = %s;
        '''

        # Execute the SQL command
        cursor.execute(query, (problem_id,))

        # Fetch the row from the database
        row = cursor.fetchone()

        # If a row is found, return it as a dictionary
        if row:
            problem_metadata = {
                "problemId": row[0],
                "problemTitle": row[1],
                "difficulty": row[2],
                "Tags": row[3],
                "description": row[4]
            }
            return problem_metadata
        else:
            print(f"No data found for problemId: {problem_id}")
            return None

    except Exception as e:
        print("Error: unable to fetch data", e)
        return None

def insert_problem_metadata(
        problemTitle: str,
        difficulty: str,
        problemId: Optional[int] = None,
        Tags: Optional[List[str]] = None,
        timeLimit: Optional[float] = None,
        memoryLimit: Optional[float] = None,
        s3_path: Optional[str] = None,
        description: Optional[str] = None
):
    try:
        # Modify the query to include the problemId and use NULL on SQL side if it's not provided
        query = '''
        INSERT INTO public."ProblemMetadata" ("problemId", "problemTitle", difficulty, "Tags", "timeLimit", "memoryLimit", s3_path, description)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
        '''
        cursor.execute(query, (problemId if problemId is not None else 'DEFAULT', problemTitle, difficulty, Tags, timeLimit, memoryLimit, s3_path, description))
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e

    finally:
        # Close the database connection
        if conn is not None:
            conn.close()