from db_connection import fetch_problems_metadata

problems_metadata = fetch_problems_metadata()
for problem in problems_metadata:
    print(problem)
