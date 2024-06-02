import pandas as pd
import re
import logging
from db_utils import connect_db, run_query, close_connection

def clean_numeric(value):
    if pd.isna(value) or value in ['N/A', '', ' ', None]:
        return None 

    if isinstance(value, str):
        if re.search(r'[a-zA-Z]', value):
            with open('problematic_values.txt', 'a', encoding='utf-8') as log_file:
                log_file.write(f"Problematic value (contains letters): {value}\n")
            return None
        
        value_cleaned = re.sub(r'[^\d,.-]', '', value)
        
        if ',' in value_cleaned and '.' in value_cleaned:
            if value_cleaned.rfind('.') > value_cleaned.rfind(','):
                value_cleaned = value_cleaned.replace(',', '')
            else:
                value_cleaned = value_cleaned.replace('.', '').replace(',', '.')
        else:
            value_cleaned = value_cleaned.replace(',', '')

        try:
            cleaned_value = float(value_cleaned)
            return cleaned_value
        except ValueError:
            return None
    else:
        try:
            return float(value) if value else None
        except ValueError:
            return None


def process_data(file_path, csv_type, mappings):
    df = pd.read_csv(file_path)
    conn = connect_db()
    cursor = conn.cursor()

    for _, row in df.iterrows():

        process_row(row, cursor, csv_type, mappings)
    conn.commit()
    
    cursor.close()
    close_connection(conn)

def get_string_value(row, column_name):
    # check if the column exists in the row and is not NaN
    if column_name in row and not pd.isna(row[column_name]):
        value = str(row[column_name]).strip()
        # check if the value is empty or contains only whitespace
        if value == "" or value.isspace():
            return None
        return value.upper()  # return the value in uppercase to match the data
    else:
        return None  


def get_number_value(row, column_name):
    # check if the column exists in the row
    if column_name in row:
        if pd.isna(row[column_name]): # check if the value is NaN
            return None
        else:
            return clean_numeric(row[column_name]) # clean the value and return it
    else:
        return None


def process_row(row, cursor, csv_type, mappings):
    # insert the data into the database
    role_id = insert_role(row, cursor, csv_type, mappings)
    company_id = insert_company(row, cursor, csv_type, mappings)
    location_id = insert_location(row, cursor, csv_type, mappings)
    employee_id = insert_employee(row, cursor, csv_type, mappings, role_id, company_id, location_id)
    insert_compensation(row, cursor, csv_type, mappings, employee_id, role_id)

def insert_role(row, cursor, csv_type, mappings):
    # get the values from the row based on the column names in the mappings
    job_title = get_string_value(row, mappings.get('job_title', ''))
    industry = get_string_value(row, mappings.get('industry', ''))
    employment_type = get_string_value(row, mappings.get('employment_type', ''))
    highest_level_of_education = get_string_value(row, mappings.get('highest_level_of_education', ''))
    
    # check if the role already exists in the database
    sql = """
    SELECT id FROM roles WHERE job_title = %s AND industry = %s AND employment_type = %s 
    """
    
    role_id = run_query(cursor, sql, (job_title, industry, employment_type))
    if role_id is None:
        sql = """
        INSERT INTO roles (job_title, industry, employment_type) VALUES (%s, %s, %s)
        RETURNING id;
        """
        role_id = run_query(cursor, sql, (job_title, industry, employment_type), is_insert=True)

    return role_id
    

def insert_company(row, cursor, csv_type, mappings):
    # get the values from the row based on the column names in the mappings
    company_name = get_string_value(row, mappings.get('company_name', ''))
    if company_name is None:
        return None
    
    company_size= get_string_value(row, mappings.get('company_size', '')) 
    industry = get_string_value(row, mappings.get('industry', ''))  
    public_or_private = get_string_value(row, mappings.get('public_or_private', ''))
    # check if the company already exists in the database
    sql = """
    SELECT id FROM companies WHERE company_name = %s AND company_size = %s AND industry = %s AND public_or_private = %s

    """
    company_id = run_query(cursor, sql, (company_name, company_size, industry, public_or_private), is_insert=True)

    if company_id is None:
        sql = """
        INSERT INTO companies (company_name, company_size, industry, public_or_private) VALUES (%s, %s, %s, %s)
        RETURNING id;
        """
        company_id = run_query(cursor, sql, (company_name, company_size, industry, public_or_private), is_insert=True)

    return company_id

def insert_location(row, cursor, csv_type, mappings):
    # the csvs have different columns for location and different formats so we need to handle them separately
    if csv_type == 'csv1':
        location= get_string_value(row, mappings.get('location', ''))
        location_city = None 
        location_country = None
    elif csv_type == 'csv2':
        location_city = get_string_value(row, mappings.get('location_city', '')) 
        location_country = get_string_value(row, mappings.get('location_country', '')) 
        location = f"{location_city}, {location_country}"
    # check if the location already exists in the database
    sql = """
    SELECT id FROM locations WHERE full_location = %s AND city = %s AND country = %s

    """

    location_id = run_query(cursor, sql, (location, location_city, location_country))
    
    if location_id is None:
        sql = """
        INSERT INTO locations (city, country, full_location) VALUES (%s, %s, %s)
        RETURNING id;
        """
        location_id = run_query(cursor, sql, (location_city, location_country, location), is_insert=True)
    
    return location_id

def insert_employee(row, cursor, csv_type, mappings, role_id, company_id, location_id):
    # get the values from the row based on the column names in the mappings
    age = get_string_value(row, mappings.get('age', ''))
    gender = get_string_value(row, mappings.get('gender', ''))
    highest_level_of_education = get_string_value(row, mappings.get('highest_level_of_education', ''))
    sql = """
    INSERT INTO employees (age, gender, location_id, role_id, company_id,highest_level_of_education) VALUES (%s, %s, %s, %s, %s, %s)
    RETURNING id;
    """
    employee_id = run_query(cursor, sql, (age, gender, location_id, role_id, company_id,highest_level_of_education), is_insert=True)

    return employee_id 

def get_currency(row, column_name, csv_type):
    # csv2 is based in USD so we can return USD directly
    if csv_type=='csv2':
        return 'USD'
    else:
        if column_name in row:
            # check if the value is empty or contains only whitespace
            if pd.isna(row[column_name]):
                return None
            # check if the value is a currency code
            elif row[column_name] == 'Other':
                return get_currency(row,"If ""Other,"" please indicate the currency here: ", csv_type)
            else:
                return row[column_name].strip().upper()
    

def insert_compensation(row, cursor, csv_type, mappings, employee_id, role_id):
    base_salary = get_number_value(row, mappings.get('base_salary', ''))
    bonus = get_number_value(row, mappings.get('bonus', ''))
    stock_options = get_number_value(row, mappings.get('stock_options', ''))
    currency = get_currency(row, mappings.get('currency', ''), csv_type)
    sql = """
    INSERT INTO compensation (employee_id, role_id, base_salary, bonus, stock_options, currency) VALUES (%s, %s, %s, %s, %s, %s);
    """
    run_query(cursor, sql, (employee_id, role_id, base_salary, bonus, stock_options, currency), is_insert=True)

