from data_processing import process_data
from config import csv_mappings, surveys_csv

def main():
    print("Loaded csv_mappings:", csv_mappings)  
    for csv_type, file_path in surveys_csv.items(): 
        print(f"Processing {file_path}...")
        process_data(file_path, csv_type, csv_mappings[csv_type]) 
       
if __name__ == "__main__":
    main()