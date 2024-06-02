import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import os

# Configuration
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_USER = os.getenv('DB_USER', 'postgres')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'postgres')


# Function to establish a connection to the database
def connect_db(dbname="postgres"):
    conn = psycopg2.connect(host=DB_HOST, dbname=dbname, user=DB_USER, password=DB_PASSWORD)
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    return conn

def create_database():
    with connect_db() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT 1 FROM pg_catalog.pg_database WHERE datname = 'compensation_db'")
            if not cur.fetchone():
                cur.execute("CREATE DATABASE compensation_db")



# Function to drop existing tables if they exist
def drop_tables(cursor):
    cursor.execute("""
        DROP TABLE IF EXISTS compensation, employment, employees, companies, roles , exchange_rates CASCADE;
    """)

# First, create the roles table because it is referenced by the employees table
def create_tables():
    with connect_db() as conn:
        with conn.cursor() as cur:
            drop_tables(cur)
            cur.execute("""
                CREATE TABLE IF NOT EXISTS companies(
                    id SERIAL PRIMARY KEY,
                    company_name VARCHAR(255),
                    company_size VARCHAR(255),
                    industry VARCHAR(255),
                    public_or_private VARCHAR(255)
                );
            """)
            
            
            cur.execute("""
                CREATE TABLE IF NOT EXISTS roles(
                    id SERIAL PRIMARY KEY,
                    job_title VARCHAR(255),
                    industry VARCHAR(255),
                    employment_type VARCHAR(255)
                );
            """)

            cur.execute("""
                CREATE TABLE IF NOT EXISTS locations(
                    id SERIAL PRIMARY KEY,
                    city VARCHAR(255),
                    country VARCHAR(255),
                    full_location VARCHAR(255)
                );
            """)

            cur.execute("""
                CREATE TABLE IF NOT EXISTS employees(
                    id SERIAL PRIMARY KEY,
                    age VARCHAR(255),
                    gender VARCHAR(255),
                    highest_level_of_education VARCHAR(255),
                    role_id INTEGER,
                    company_id INTEGER,
                    location_id INTEGER,
                    CONSTRAINT fk_role FOREIGN KEY(role_id) REFERENCES roles(id) ON DELETE SET NULL,
                    CONSTRAINT fk_company FOREIGN KEY(company_id) REFERENCES companies(id) ON DELETE SET NULL,
                    CONSTRAINT fk_location FOREIGN KEY(location_id) REFERENCES locations(id) ON DELETE SET NULL
                );
            """)

            cur.execute("""
                CREATE TABLE IF NOT EXISTS compensation(
                    id SERIAL PRIMARY KEY,
                    employee_id INTEGER REFERENCES employees(id),
                    role_id INTEGER REFERENCES roles(id),
                    base_salary DECIMAL,
                    bonus DECIMAL,
                    stock_options DECIMAL,
                    currency VARCHAR(10)
                );
            """)
            cur.execute("""
                CREATE TABLE IF NOT EXISTS exchange_rates (
                    currency VARCHAR(10) PRIMARY KEY,
                    rate_to_usd DECIMAL
            );
            """)
            conn.commit()



def insert_exchange_rates():
    exchange_rates = {
        'USD': 1.0,     
        'EUR': 1.09,      
        'GBP': 1.27,
        'JPY': 0.006,
        'CAD': 0.73,
        'ZAR': 0.053,
        'CHF': 1.11,
        'HKD': 0.13,
        'SEK': 0.1,
    }

    conn = connect_db()
    cur = conn.cursor()

    for currency, rate in exchange_rates.items():
        cur.execute("""
            INSERT INTO exchange_rates (currency, rate_to_usd)
            VALUES (%s, %s)
            ON CONFLICT (currency) DO UPDATE SET rate_to_usd = EXCLUDED.rate_to_usd
        """, (currency, rate))

    conn.commit()
    cur.close()
    conn.close()


def main():
    """Main function to run all tasks."""
    create_database()
    create_tables()
    insert_exchange_rates()


if __name__ == '__main__':
    main()

