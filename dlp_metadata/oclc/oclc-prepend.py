import os
import csv
import re

# Function to find and process CSV files in a folder and its subfolders
def process_csv_files(folder_path):
    # Regular expression pattern to match column headings containing 'oclc' (case-insensitive)
    oclc_pattern = re.compile(r'.*oclc.*', re.IGNORECASE)

    edited_files = []  # Store the names of edited CSV files

    # Walk through the folder and its subfolders
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith(".csv"):
                file_path = os.path.join(root, file)
                with open(file_path, 'r', newline='') as csvfile:
                    reader = csv.reader(csvfile)
                    headers = next(reader)  # Read the headers

                    # Find the column indices that match the oclc pattern
                    oclc_columns = [i for i, header in enumerate(headers) if oclc_pattern.match(header)]

                    # If there are oclc columns, process the file
                    if oclc_columns:
                        data = list(reader)
                        edited = False  # Flag to track if any value was edited
                        for row in data:
                            for col_index in oclc_columns:
                                if row[col_index]:
                                    edited = True  # Set the flag to True
                                    row[col_index] = 'OCLC: ' + row[col_index]

                        # If any value was edited, write the modified data back to the CSV
                        if edited:
                            with open(file_path, 'w', newline='') as output_csvfile:
                                writer = csv.writer(output_csvfile)
                                writer.writerow(headers)
                                writer.writerows(data)

                            edited_files.append(file)  # Record the name of the edited file

    # Print the names of edited CSV files
    if edited_files:
        print("Edited CSV files:")
        for file in edited_files:
            print(file)

# Input: Specify the folder path where CSVs are located
folder_path = input("Enter the folder path where CSVs are located: ")

# Call the function to process CSV files
process_csv_files(folder_path)
