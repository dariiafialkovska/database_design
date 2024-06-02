import psycopg2
import csv

def compensation_by_gender():
    conn = psycopg2.connect(host="localhost", dbname="compensation_db", user="postgres", password="postgres")
    cur = conn.cursor()
    
    query = """
    SELECT e.gender,AVG(c.base_salary + COALESCE(c.bonus, 0) + COALESCE(c.stock_options, 0)) AS average_compensation,
    COUNT(*) AS num_entries FROM employees e 
    JOIN compensation c ON e.id = c.employee_id
    WHERE e.gender IS NOT NULL AND TRIM(e.gender) <> ''
    GROUP BY e.gender
    ORDER BY num_entries DESC;
    """
    cur.execute(query)
    rows = cur.fetchall()
    csv_file_path = 'average_compensation_by_gender.csv'
    
    with open(csv_file_path, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(['Gender', 'Average Compensation (USD)', 'Number of Entries'])
        for row in rows:
            gender_label = row[0] if row[0] is not None else "Unspecified"
            csvwriter.writerow([gender_label, f"{row[1]:,.2f}", row[2]])
    cur.close()
    conn.close()


def compensation_by_role_engineer():
    conn = psycopg2.connect(host="localhost", dbname="compensation_db", user="postgres", password="postgres")
    cur = conn.cursor()
    
    query = """
    SELECT r.job_title,AVG(COALESCE(c.base_salary, 0) + COALESCE(c.bonus, 0) + COALESCE(c.stock_options, 0)) * AVG(COALESCE(er.rate_to_usd, 1)) AS average_compensation,
    COUNT(*) AS num_engineers
    FROM roles r
    JOIN compensation c ON r.id = c.role_id
    JOIN exchange_rates er ON c.currency = er.currency
    WHERE r.job_title ILIKE '%engineer%'
    AND (c.base_salary IS NOT NULL OR c.bonus IS NOT NULL OR c.stock_options IS NOT NULL)  
    GROUP BY r.job_title
    HAVING COUNT(c.base_salary) > 0 OR COUNT(c.bonus) > 0 OR COUNT(c.stock_options) > 0
    ORDER BY average_compensation DESC;
    """
    
    cur.execute(query)
    rows = cur.fetchall()
    csv_file_path = 'average_compensation_for_engineers.csv'

    with open(csv_file_path, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(['Job Title', 'Average Compensation (USD)', 'Number of Engineers'])
        for row in rows:
            if row[1] is not None: 
                formatted_row = [row[0], f"{row[1]:.2f}", row[2]] 
                csvwriter.writerow(formatted_row)
    cur.close()
    conn.close()

def compensation_by_city():
    conn = psycopg2.connect(host="localhost", dbname="compensation_db", user="postgres", password="postgres")
    cur = conn.cursor()
    
    query = """
    SELECT l.city,
        AVG(c.base_salary + COALESCE(c.bonus, 0) + COALESCE(c.stock_options, 0)) AS average_compensation,
        MIN(c.base_salary + COALESCE(c.bonus, 0) + COALESCE(c.stock_options, 0)) AS min_compensation,
        MAX(c.base_salary + COALESCE(c.bonus, 0) + COALESCE(c.stock_options, 0)) AS max_compensation
    FROM employees e
    JOIN compensation c ON e.id = c.employee_id
    JOIN locations l ON e.location_id = l.id
    WHERE l.city IS NOT NULL AND TRIM(l.city) <> ''  -- Ensure city is not null or empty
    GROUP BY l.city
    ORDER BY l.city;
    """
    
    cur.execute(query)
    rows = cur.fetchall()
    csv_file_path = 'average_compensation_by_city.csv'

    with open(csv_file_path, 'w', newline='',encoding='utf-8') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(['City', 'Average Compensation (USD)', 'Min Compensation (USD)', 'Max Compensation (USD)'])
        for row in rows:
            csvwriter.writerow([row[0], f"{row[1]:,.2f}", f"{row[2]:,.2f}", f"{row[3]:,.2f}"])


    cur.close()
    conn.close()


def main():
    compensation_by_gender()
    compensation_by_role_engineer()
    compensation_by_city()


if __name__ == "__main__":
    main()