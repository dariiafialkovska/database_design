import psycopg2

def connect_db():
    try:
        connection = psycopg2.connect(host="localhost", dbname="compensation_db", user="postgres", password="postgres")
        return connection
    except psycopg2.DatabaseError as e:
        print(f"Database connection failed: {e}")
        raise

def run_query(cursor, sql, params=None, is_insert=False):
    cursor.execute(sql, params)
    if is_insert:
        try:
            result = cursor.fetchone()
            return result[0] if result else None
        except psycopg2.ProgrammingError as e:
            return None
    else:
        return cursor.fetchone()  


def close_connection(connection):
    if connection:
        connection.close()
        print("Database connection closed")
