import os
import csv
import re

def sanitize_filename(value):
    # Replace special characters with underscores and remove other invalid characters
    sanitized_value = re.sub(r'[^a-zA-Z0-9_-]', '_', value)
    return sanitized_value

def split_csv_by_value(input_file, column_name):
    # Create a directory to store the split CSVs
    output_dir = 'split_csvs'
    os.makedirs(output_dir, exist_ok=True)

    with open(input_file, 'r') as file:
        reader = csv.DictReader(file)
        
        # Create a dictionary to store the output CSV writers
        writers = {}

        for row in reader:
            value = row[column_name]  # Get the value from the specified column
            sanitized_value = sanitize_filename(value)

            if sanitized_value not in writers:
                # Create a new CSV writer for the value if it doesn't exist
                output_file = os.path.join(output_dir, f'{sanitized_value}.csv')
                writers[sanitized_value] = csv.writer(open(output_file, 'w', newline=''))
                writers[sanitized_value].writerow(reader.fieldnames)  # Write the header row to the new CSV

            # Write the row to the appropriate CSV
            writers[sanitized_value].writerow(row.values())

    print(f'Successfully split the CSV into multiple files in the "{output_dir}" directory.')

# Prompt for the path to the input CSV file
input_file = input('Enter the path to the CSV file: ')

# Specify the name of the column to split by
column_name = 'Parent ARK'  # You can modify this if needed

split_csv_by_value(input_file, column_name)

